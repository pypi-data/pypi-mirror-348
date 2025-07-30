"""certgrinder.py tests.

Runs with pytest and Tox.
"""

import base64
import binascii
import copy
import hashlib
import logging
import pathlib
import ssl
import subprocess
import time
import urllib.request
from collections.abc import Iterator
from pathlib import Path
from typing import Any, NamedTuple

import dns.resolver
import pytest
from cryptography import x509
from cryptography.hazmat import primitives
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.x509.oid import NameOID

import certgrinder.certgrinder
from certgrinder.certgrinder import Certgrinder, main, parse_args


class DNSResponse(NamedTuple):
    """A mock response for use with mock dns.resolver.query functions."""

    usage: int
    selector: int
    mtype: int
    cert: bytes


def delete_argparse_keys(config: dict[str, str]) -> dict[str, str]:
    """Delete keys that are part of argparse internals."""
    for key in ["command", "subcommand", "method"]:
        config.pop(key, None)
    return config


def test_certgrinderd_broken_configfile(
    tmpdir_factory: pytest.TempdirFactory, caplog: pytest.LogCaptureFixture, certgrinderd_broken_yaml_configfile: Path
) -> None:
    """Test certgrinderd with a broken config."""
    mockargs = [
        "--path",
        str(tmpdir_factory.mktemp("certificates")),
        "--domain-list",
        "example.com,www.example.com",
        "--certgrinderd",
        f"server/certgrinderd/certgrinderd.py --config-file {certgrinderd_broken_yaml_configfile}",
        "--debug",
        "get",
        "certificate",
    ]
    with pytest.raises(SystemExit) as e:
        main(mockargs)
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert "Unable to parse YAML config file" in caplog.text
    # make sure we dont leak any of the file in the backtrace
    assert "foo:" not in caplog.text
    assert "bar" not in caplog.text


def test_certgrinderd_fail(
    tmpdir_factory: pytest.TempdirFactory, certgrinderd_env: None, caplog: pytest.LogCaptureFixture
) -> None:
    """Test a failing certbot."""
    mockargs = [
        "--path",
        str(tmpdir_factory.mktemp("certificates")),
        "--domain-list",
        "example.com,www.example.com",
        "--certgrinderd",
        "server/certgrinderd/certgrinderd.py --certbot-command /bin/false --acme-zone acme.example.com",
        "--debug",
        "get",
        "certificate",
    ]
    with pytest.raises(SystemExit) as e:
        main(mockargs)
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert "certbot command returned non-zero exit code" in caplog.text


def test_certgrinderd_broken_csr(
    csr_with_two_cn: str, certgrinderd_env: None, certgrinderd_configfile: tuple[str, Path]
) -> None:
    """Test calling certgrinderd with an invalid CSR."""
    if certgrinderd_configfile[0] != "dns":
        # we only need to test this once
        return

    p = subprocess.Popen(
        [
            "server/certgrinderd/certgrinderd.py",
            "--config-file",
            certgrinderd_configfile[1],
            "get",
            "certificate",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # send the CSR to stdin and save stdout (the cert chain) + stderr (the certgrinderd logging)
    certgrinderd_stdout, certgrinderd_stderr = p.communicate(input=csr_with_two_cn.encode("ASCII"))
    assert p.returncode == 1
    assert "CSR is not valid (has more or less than 1 CN), bailing out" in certgrinderd_stderr.decode("ASCII"), (
        "Did not find expected error message with broken CSR"
    )


def test_get_certificate(  # noqa: PLR0913, PLR0915
    pebble_server_build: Path,
    pebble_server_run: Iterator[str],
    pebble_issuer: tuple[Path, Path],
    certgrinderd_configfile: tuple[str, Path],
    certgrinderd_env: None,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    """Get a couple of certificates and check that they look right."""
    caplog.set_level(logging.DEBUG)

    mockargs = [
        "--path",
        str(tmpdir_factory.mktemp("certificates")),
        "--domain-list",
        "example.com,www.example.com",
        "--domain-list",
        "example.net,blåbærsyltetøj.example.net",
        "--domain-list",
        "pølse.dk",
        "--certgrinderd",
        f"server/certgrinderd/certgrinderd.py --config-file {certgrinderd_configfile[1]} --acme-server-url https://127.0.0.1:14000/dir ",
        "--debug",
    ]

    if certgrinderd_configfile[0] == "dns":
        # include a couple of post renew hook for one of the cert operations
        mockargs += ["--post-renew-hooks", "true", "--post-renew-hooks", "false"]
    elif certgrinderd_configfile[0] == "http":
        # include post-renew-hooks-dir for one of the cert operations
        hookdir = Path(tmpdir_factory.mktemp("hooks"))
        mockargs += [
            "--post-renew-hooks-dir",
            str(hookdir),
            "--post-renew-hooks-dir-runner",
            "/bin/echo",
        ]
        # write mock hooks to hook dir
        with (hookdir / "hooktrue").open("w") as f:
            f.write("#!/bin/sh\n/bin/true\n")
        (hookdir / "hooktrue").chmod(0o0755)
        with (hookdir / "hookfalse").open("w") as f:
            f.write("#!/bin/sh\n/bin/false\n")
        (hookdir / "hookfalse").chmod(0o0755)

    with pytest.raises(SystemExit) as e:
        main([*mockargs, "get", "certificate"])
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"

    # initialise a TLS context with the pebble minica.pem to download certs
    tls_context = ssl.create_default_context(cafile=str(pebble_server_build / "test/certs/pebble.minica.pem"))

    # download issuer cert
    with urllib.request.urlopen("https://127.0.0.1:15000/intermediates/0", context=tls_context) as u:
        issuer = x509.load_pem_x509_certificate(u.read(), default_backend())

    # only check certs if we expect to get any
    if certgrinderd_configfile[0] == "":
        assert "No more challenge types to try, unable to get certificate" in caplog.text, (
            "Did not find expected errormessage with no challenge types enabled"
        )
    else:
        # check that the certificates were issued correctly
        for keytype in ["rsa", "ecdsa"]:
            for domainset in [
                "example.com,www.example.com",
                "example.net,blåbærsyltetøj.example.net",
                "pølse.dk".encode("idna").decode("ascii"),
            ]:
                domains = domainset.split(",")
                certpath = Path(mockargs[1], domains[0] + f"-certificate.{keytype}.crt")
                with certpath.open("rb") as f:
                    certificate = x509.load_pem_x509_certificate(f.read(), default_backend())
                # check that it was issued by our issuer
                assert issuer.subject == certificate.issuer
                # check that the cert has the right CN in subject
                name = x509.NameAttribute(NameOID.COMMON_NAME, domains[0].encode("idna").decode("ascii"))
                cns = certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
                assert len(cns) == 1, "Certificate must have exactly one CN attribute"
                assert cns[0] == name, "Certificate CN does not match expected name"
                # make sure we have the full domainlist in SubjectAltName
                assert [
                    d.encode("idna").decode("ascii") for d in domains
                ] == certificate.extensions.get_extension_for_oid(
                    x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
                ).value.get_values_for_type(x509.DNSName), (
                    "SubjectAltName extension does not contain the right list of domains."
                )

                with pytest.raises(SystemExit) as e:
                    main([*mockargs, "show", "certificate"])
                assert str(certificate.serial_number) in caplog.text
                assert str(certificate.subject) in caplog.text

            if keytype == "ecdsa":
                # delete the certificate and issuer to test the cert/issuer splitter
                certificate_path = Path(mockargs[1], domains[0] + f"-certificate.{keytype}.crt")
                certificate_path.unlink()
                issuer_path = Path(mockargs[1], domains[0] + f"-issuer.{keytype}.crt")
                issuer_path.unlink()

        # we only need to test CAA once
        if certgrinderd_configfile[0] == "dns":
            certpath = Path(tmpdir_factory.mktemp("certificates"))
            # make sure the "show caa" subcommand works,
            # this requires pebble running with a registered account,
            # so it is placed here instead of a seperate test
            caplog.clear()
            mockargs = [
                "--path",
                str(certpath),
                "--domain-list",
                "example.com,www.example.com",
                "--domain-list",
                "*.example.org",
                "--certgrinderd",
                f"server/certgrinderd/certgrinderd.py --config-file {certgrinderd_configfile[1]} --acme-server-url https://127.0.0.1:14000/dir",
                "--debug",
            ]
            with pytest.raises(SystemExit) as e:
                main([*mockargs, "show", "caa"])
            assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
            captured = capsys.readouterr()
            assert (
                'example.com IN CAA 128 issue "letsencrypt.org; validationmethods=dns-01,http-01; accounturi=https://127.0.0.1:14000/my-account/1"'
                in captured.out
            )
            assert 'example.com IN CAA 128 issuewild ";"' in captured.out
            assert (
                'www.example.com IN CAA 128 issue "letsencrypt.org; validationmethods=dns-01,http-01; accounturi=https://127.0.0.1:14000/my-account/1"'
                in captured.out
            )
            assert 'www.example.com IN CAA 128 issuewild ";"' in captured.out
            assert (
                'example.org IN CAA 128 issuewild "letsencrypt.org; validationmethods=dns-01; accounturi=https://127.0.0.1:14000/my-account/1"'
                in captured.out
            )
            assert 'example.org IN CAA 128 issue ";"' in captured.out

            # make sure the --caa-validation-methods arg works
            mockargs = [
                "--path",
                str(certpath),
                "--domain-list",
                "example.com",
                "--certgrinderd",
                f"server/certgrinderd/certgrinderd.py --config-file {certgrinderd_configfile[1]} --acme-server-url https://127.0.0.1:14000/dir",
                "--caa-validation-methods",
                "dns-01",
                "--debug",
            ]
            with pytest.raises(SystemExit) as e:
                main([*mockargs, "show", "caa"])
            assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
            captured = capsys.readouterr()
            assert (
                'example.com IN CAA 128 issue "letsencrypt.org; validationmethods=dns-01; accounturi=https://127.0.0.1:14000/my-account/1"'
                in captured.out
            )


def test_show_spki(caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory) -> None:
    """Test the 'show spki' subcommand."""
    # SPKI is output at level INFO
    caplog.set_level(logging.INFO)
    parser, args = parse_args(
        [
            "--certgrinder",
            "true",
            "--path",
            str(tmpdir_factory.mktemp("certificates")),
            "--domain-list",
            "example.com,www.example.com",
            "show",
            "spki",
        ]
    )
    certgrinder = Certgrinder()
    config = copy.deepcopy(vars(args))
    config = delete_argparse_keys(config)
    certgrinder.configure(userconfig=config)
    with pytest.raises(SystemExit) as e:
        certgrinder.grind(args)
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    # load public key
    with certgrinder.keypair_path.open("rb") as f:
        keypair = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend(),
        )
    derkey = keypair.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    # calculate SPKI for the pubkey
    spki = base64.b64encode(hashlib.sha256(derkey).digest()).decode("ASCII")
    assert spki in caplog.text, "SPKI not found in output"


def test_generate_tlsa(known_public_key: RSAPublicKey) -> None:
    """Test the TLSA record generation from a known public key."""
    certgrinder = Certgrinder()

    # test with a known public key
    public_key_der_bytes = known_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    tlsa310 = "30820222300D06092A864886F70D01010105000382020F003082020A0282020100B7385B728CCD6234B579EE7918329DA988DEB18B83EA7C45422B8281F53682AC57C93AC428EB3BFF216926662CC69D34FC2D8EE44673C9C87EF8DCDFFDE93FC5F483834465F075376691DA46FB157B68E3D58E16B5A5C0FAF026A6EAADC1FD47E55C0B2E98669CD13A9A42AFC7180F88769E409A46029CCE0FE3184A66FF3A1ABBB848CF7064EF299246CA42175EFBD30FA2A2437B19EFC9DA7BCAFA74D583DA8397B84B3492E7C084AA31B49CF3CDE1A661F0B112F2676F1BA6C9EB9EB42EB104EE7F0C0859D9F0C3C5821602B7D628C2E62195D2174CEAABAA2794DAEBA0EB7C165A2B6EA146CEACA08EC0534DDBF74149C694B6D03EC8CAC8251215853B4171588C5B3D8B5BB4B9C9960F75B540A61759F44474648ACF9810ABA65519379030639769EECC782EF1D0B81E956839B23B77A753868625B6648E5E0ACFD31F40EDB7B26CB5D9EAB91FECDEB9EFEF5752F4F5E9A92C87B9D20732D13FE9077ABD5767065756C01B5264722BB2740AF5A1EE2A60B08C5814C8CED874DBCE2F034A364BC59473BCB65B6463DE3E6657C6B287B02050A005D74C4617735C27B324FAE004491BB646302940BB7239FDC997F3F5EC27CA683F1742F5C279780B32CE33D24FA11B63ED390BAC417CC1206FFF49FBCE203F9C31D9AAFA106FC7169723F00BC6A59E0142790135C131D38BF549183ECE52BC683FD42D07057BABB6259E810203010001"
    assert certgrinder.generate_tlsa_record(derkey=public_key_der_bytes, tlsatype="310") == tlsa310, (
        "Generation of DANE-EE Publickey Full (3 1 0) TLSA Record failed"
    )

    tlsa311 = "D6F9BA311A04F711C19C459266D53561145AC1ABF403E368976AFE51B41FAE53"
    assert certgrinder.generate_tlsa_record(derkey=public_key_der_bytes, tlsatype="311") == tlsa311, (
        "Generation of DANE-EE Publickey SHA256 (3 1 1) TLSA Record failed"
    )

    tlsa312 = "048D0D297B5E525795CEEBB87C8CD18436766CB87DE3B5E50EE9863DB3A12FB8E639878A4B03A0C23CC2253257266F9A695EA24207CEF284EB6FD45322AE809A"
    assert certgrinder.generate_tlsa_record(derkey=public_key_der_bytes, tlsatype="312") == tlsa312, (
        "Generation of DANE-EE Publickey SHA512 (3 1 2) TLSA Record failed"
    )

    with pytest.raises(ValueError, match="Unsupported TLSA type: 1337"):
        certgrinder.generate_tlsa_record(derkey=public_key_der_bytes, tlsatype="1337")


def test_generate_spki(known_public_key: RSAPublicKey) -> None:
    """Test the SPKI pin-sha256 record generation from a known public key."""
    certgrinder = Certgrinder()

    # test with a known public key
    public_key_der_bytes = known_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    spki = "1vm6MRoE9xHBnEWSZtU1YRRawav0A+Nol2r+UbQfrlM="
    assert certgrinder.generate_spki(derkey=public_key_der_bytes) == spki, "SPKI pin-sha256 generation failed"


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the version command."""
    with pytest.raises(SystemExit) as e:
        main(["version"])
    assert e.type is SystemExit
    captured = capsys.readouterr()
    assert captured.out == f"Certgrinder version {Certgrinder.__version__}\n"


def test_argparse() -> None:
    """Test argparse works as expected."""
    parser, args = parse_args(["-D", "example.com", "show", "tlsa", "443", "tcp"])
    assert isinstance(getattr(args, "domain-list"), list)
    assert getattr(args, "domain-list") == ["example.com"]
    assert args.command == "show"
    assert args.subcommand == "tlsa"
    assert getattr(args, "tlsa-port") == 443
    assert getattr(args, "tlsa-protocol") == "tcp"


def test_no_domainlist(caplog: pytest.LogCaptureFixture) -> None:
    """Test Certgrinder with no domain-list config."""
    certgrinder = Certgrinder()
    with pytest.raises(SystemExit) as e:
        certgrinder.configure({})
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert "No domain-list(s) configured." in caplog.text


def test_no_path(caplog: pytest.LogCaptureFixture) -> None:
    """Test Certgrinder with no path in config."""
    certgrinder = Certgrinder()
    with pytest.raises(SystemExit) as e:
        certgrinder.configure({"domain-list": ["example.com"], "certgrinderd": "true"})
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert "No configured path" in caplog.text


def test_nonexistant_path(caplog: pytest.LogCaptureFixture) -> None:
    """Test Certgrinder with wrong path setting."""
    certgrinder = Certgrinder()
    with pytest.raises(SystemExit) as e:
        certgrinder.configure(
            {
                "domain-list": ["example.com,www.example.com"],
                "path": "/nonexistant",
                "certgrinderd": "true",
            }
        )
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert "Configured path /nonexistant does not exist" in caplog.text


def test_permission_denied_path(caplog: pytest.LogCaptureFixture) -> None:
    """Test Certgrinder with a path with no permissions."""
    certgrinder = Certgrinder()
    with pytest.raises(SystemExit) as e:
        certgrinder.configure(
            {
                "domain-list": ["example.com,www.example.com"],
                "path": "/dev",
                "certgrinderd": "true",
            }
        )
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert "Permission error while accessing configured path" in caplog.text


def test_syslog_connect(tmpdir_factory: pytest.TempdirFactory, caplog: pytest.LogCaptureFixture) -> None:
    """Test syslog connect functionality."""
    certgrinder = Certgrinder()
    certgrinder.configure(
        {
            "domain-list": ["example.com,www.example.com"],
            "path": str(tmpdir_factory.mktemp("certificates")),
            "syslog-socket": "/dev/log",
            "syslog-facility": "LOG_LOCAL0",
            "certgrinderd": "true",
        }
    )


def test_syslog_connect_wrong_socket(tmpdir_factory: pytest.TempdirFactory, caplog: pytest.LogCaptureFixture) -> None:
    """Test syslog connect functionality."""
    certgrinder = Certgrinder()
    with pytest.raises(FileNotFoundError):
        certgrinder.configure(
            {
                "domain-list": ["example.com,www.example.com"],
                "path": str(tmpdir_factory.mktemp("certificates")),
                "syslog-socket": "/dev/notlog",
                "syslog-facility": "LOG_LOCAL0",
                "certgrinderd": "true",
            }
        )


def test_create_and_chmod_keypair(tmpdir_factory: pytest.TempdirFactory, caplog: pytest.LogCaptureFixture) -> None:
    """Test generating ed2519 keypair, and chmod correcting."""
    certgrinder = Certgrinder()
    with pytest.raises(TypeError, match="Unsupported keytype"):
        keypair = certgrinder.generate_private_key("foo")
    keypair = certgrinder.generate_private_key("ed25519")
    assert isinstance(keypair, primitives.asymmetric.ed25519.Ed25519PrivateKey)
    path = Path(tmpdir_factory.mktemp("certificates") / "test.key")
    with pytest.raises(TypeError, match="Unsupported keytype"):
        certgrinder.save_keypair(keypair="notakey", path=path)  # type: ignore[arg-type]
    certgrinder.save_keypair(keypair=keypair, path=path)
    assert oct(path.stat().st_mode)[4:] == "0640", "Keypair saved with wrong permissions"
    path.chmod(0o777)
    # loading the keypair should fix the mode to 0640
    certgrinder.load_keypair(path)
    assert oct(path.stat().st_mode)[4:] == "0640", "Keypair saved with wrong permissions"
    assert "has incorrect permissions, fixing to 0640" in caplog.text


def test_check_certificate_issuer_empty_invalid_ca_cn_list(
    signed_certificate: x509.Certificate, caplog: pytest.LogCaptureFixture
) -> None:
    """Test the check_certificate_issuer() method with an empty invalid_ca_cn_list."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    assert certgrinder.check_certificate_issuer(certificate=signed_certificate, invalid_ca_cn_list=[]) is True, (
        "check_certificate_issuer() did not return True with an empty invalid_ca_cn_list"
    )
    assert "We have an empty invalid_ca_cn_list, returning True" in caplog.text


def test_check_certificate_issuer_selfsigned(
    selfsigned_certificate: x509.Certificate, caplog: pytest.LogCaptureFixture
) -> None:
    """Test the check_certificate_issuer() method with a selfsigned cert."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    assert (
        certgrinder.check_certificate_issuer(certificate=selfsigned_certificate, invalid_ca_cn_list=["badca"]) is False
    ), "check_certificate_issuer() did not return False with a selfsigned cert"
    assert "This certificate is selfsigned, returning False" in caplog.text


def test_check_certificate_issuer_invalid_ca(
    signed_certificate: x509.Certificate, caplog: pytest.LogCaptureFixture
) -> None:
    """Test the check_certificate_issuer() method with a cert issued by an invalid CA."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    assert (
        certgrinder.check_certificate_issuer(certificate=signed_certificate, invalid_ca_cn_list=["example.net"])
        is False
    ), "check_certificate_issuer() did not return False when checking a cert issued by a CA in the invalid_ca_cn_list"
    assert "This certificate was issued by a CA CN" in caplog.text


def test_check_certificate_expiry(selfsigned_certificate: x509.Certificate, caplog: pytest.LogCaptureFixture) -> None:
    """Test the check_certificate_expiry() method with a cert valid for 10 days."""
    assert Certgrinder().check_certificate_expiry(certificate=selfsigned_certificate, threshold_days=30) is False, (
        "check_certficate_expiry() did not return False with a cert with 10 days validity"
    )


def test_check_certificate_validity(
    selfsigned_certificate: x509.Certificate,
    signed_certificate: x509.Certificate,
    known_public_key: RSAPublicKey,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the various failure modes of the check_certificate_validity() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()

    assert (
        certgrinder.check_certificate_validity(
            certificate=signed_certificate,
            invalid_ca_cn_list=["example.net"],
            threshold_days=30,
            san_names=["example.com"],
        )
        is False
    ), "check_certificate_validity() did not return False when checking a cert issued by a CA in the invalid_ca_cn_list"
    assert "CN is on our list of invalid CAs" in caplog.text
    caplog.clear()

    assert (
        certgrinder.check_certificate_validity(
            certificate=signed_certificate,
            invalid_ca_cn_list=["badca"],
            threshold_days=100,
            san_names=["example.com"],
        )
        is False
    ), (
        "check_certificate_validity() did not return False when checking a cert with 90 days validity when the threshold is 100"
    )
    assert "Certificate expires in less than" in caplog.text
    caplog.clear()

    assert (
        certgrinder.check_certificate_validity(
            certificate=signed_certificate,
            invalid_ca_cn_list=["badca"],
            threshold_days=30,
            san_names=["example.com"],
            public_key=known_public_key,
        )
        is False
    ), "check_certificate_validity() did not return False when checking a cert with a wrong public key"
    assert "Certificate public key is different from the expected" in caplog.text
    caplog.clear()

    assert (
        certgrinder.check_certificate_validity(
            certificate=signed_certificate,
            invalid_ca_cn_list=["badca"],
            threshold_days=30,
            san_names=["example.com"],
            subject=x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "wrong")]),
        )
        is False
    ), "check_certificate_validity() did not return False when checking a cert with a wrong subject"
    assert "Certificate subject is different from the expected" in caplog.text
    caplog.clear()

    assert (
        certgrinder.check_certificate_validity(
            certificate=signed_certificate,
            invalid_ca_cn_list=["badca"],
            threshold_days=30,
            san_names=["example.org"],
        )
        is False
    ), "check_certificate_validity() did not return False when checking a cert with a wrong san_names list"
    assert "Certificate SAN name list is different from the expected" in caplog.text


def test_get_certgrinderd_command_staging(
    tmpdir_factory: pytest.TempdirFactory, certgrinderd_configfile: tuple[str, Path], caplog: pytest.LogCaptureFixture
) -> None:
    """Make sure we use the staging url when using --staging."""
    caplog.set_level(logging.DEBUG)
    parser, args = parse_args(
        [
            "--path",
            str(tmpdir_factory.mktemp("certificates")),
            "--domain-list",
            "example.com,www.example.com",
            "--certgrinderd",
            f"server/certgrinderd/certgrinderd.py --config-file {certgrinderd_configfile[1]}",
            "--staging",
            "get",
            "certificate",
        ]
    )
    certgrinder = Certgrinder()
    config = copy.deepcopy(vars(args))
    config = delete_argparse_keys(config)
    certgrinder.configure(userconfig=config)
    command = certgrinder.get_certgrinderd_command(subcommand=["get", "certificate"])
    assert "https://acme-staging-v02.api.letsencrypt.org/directory" in command
    assert "invalid_ca_cn_list=[]" in caplog.text


def test_parse_certificate_chain_not_pem(
    caplog: pytest.LogCaptureFixture,
    tmpdir_factory: pytest.TempdirFactory,
    known_csr: str,
    signed_certificate: x509.Certificate,
) -> None:
    """Test the various failure modes of the parse_certificate_chain() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
        }
    )
    csr = x509.load_pem_x509_csr(known_csr.encode("ascii"), default_backend())
    assert certgrinder.parse_certificate_chain(certificate_chain=b"NOT_A_PEM_CERT", csr=csr) is None, (
        "The parse_certificate_chain() method did not return None with a non-PEM certificate input"
    )
    assert "This is the certificate chain which failed to parse" in caplog.text
    assert "NOT_A_PEM_CERT" in caplog.text
    caplog.clear()

    stdout = b"""-----BEGIN CERTIFICATE-----
NOT_A_PEM
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
ALSO_NOT_A_PEM
-----END CERTIFICATE-----"""
    assert certgrinder.parse_certificate_chain(certificate_chain=stdout, csr=csr) is None, (
        "The parse_certificate_chain() method did not return None with a PEM-ish but invalid certificate input"
    )
    assert "This is the certificate which failed to parse" in caplog.text
    assert "NOT_A_PEM" in caplog.text
    caplog.clear()

    stdout = signed_certificate.public_bytes(primitives.serialization.Encoding.PEM)
    stdout += b"""-----BEGIN CERTIFICATE-----
ALSO_NOT_A_PEM
-----END CERTIFICATE-----"""
    assert certgrinder.parse_certificate_chain(certificate_chain=stdout, csr=csr) is None, (
        "The parse_certificate_chain() method did not return None with a non-PEM certificate input"
    )
    assert "Unable to parse, this is not a valid PEM formatted certificate." in caplog.text
    assert "This is the certificate which failed to parse" in caplog.text
    assert "ALSO_NOT_A_PEM" in caplog.text


def test_get_certificate_method(
    caplog: pytest.LogCaptureFixture,
    tmpdir_factory: pytest.TempdirFactory,
    known_csr: str,
    signed_certificate: x509.Certificate,
) -> None:
    """Test various failure modes of the get_certificate() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    certgrinder.load_domainset(certgrinder.conf.domain_list[0].split(","), keytype="ecdsa")
    csr = x509.load_pem_x509_csr(known_csr.encode("ascii"), default_backend())
    stdout = signed_certificate.public_bytes(primitives.serialization.Encoding.PEM) * 2
    assert certgrinder.get_certificate(csr=csr, stdout=stdout) is False, (
        "The get_certificate() method did not return False as expected"
    )
    assert "Certificate public key is different from the expected" in caplog.text
    assert "Certificate is not valid." in caplog.text
    assert "Did not get a certificate :(" in caplog.text


def test_check_certificate_no_file(caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory) -> None:
    """Make sure the check_certificate() method behaves if the file doesn't exist."""
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    certgrinder.load_domainset(certgrinder.conf.domain_list[0].split(","), keytype="rsa")
    assert certgrinder.check_certificate() is False, (
        "check_certificate() method did not return False as expected when called with a nonexiststant certificate path"
    )
    assert "not found" in caplog.text
    assert certgrinder.error is True, "certgrinder.error is not True as expected after an error happened"


def test_check_certificate_not_cert(caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory) -> None:
    """Make sure the check_certificate() method behaves with a file that isn't a cert."""
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    certgrinder.certificate_chain_path = pathlib.Path(__file__).absolute()
    with pytest.raises(UnicodeDecodeError, match="codec can't decode byte"):
        certgrinder.check_certificate()


def test_check_certificate_selfsigned(
    caplog: pytest.LogCaptureFixture,
    tmpdir_factory: pytest.TempdirFactory,
    selfsigned_certificate: x509.Certificate,
) -> None:
    """Make sure the check_certificate() method behaves if the cert is selfsigned."""
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    certgrinder.load_domainset(certgrinder.conf.domain_list[0].split(","), keytype="rsa")
    assert certgrinder.check_certificate(certificate=selfsigned_certificate) is False, (
        "check_certificate() method did not return False as expected when called with a selfsigned certificate"
    )
    assert certgrinder.error is True, "certgrinder.error is not True as expected after an error happened"


def test_show_certificate_file_not_found(
    caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory
) -> None:
    """Make sure the show_certificate() method logs the right error when file not found."""
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    certgrinder.certificate_path = Path("/nonexistant")
    assert certgrinder.show_certificate() is None, "show_certificate() did not return None as expected"  # type: ignore[func-returns-value]
    assert "Certificate /nonexistant not found" in caplog.text


def mock_tlsa_query_2_responses(*args: Any, **kwargs: Any) -> list[DNSResponse]:
    """A mock dns.resolver.query function which just returns 2 bogus TLSA records."""
    return [DNSResponse(3, 1, 1, b"FOO"), DNSResponse(3, 1, 2, b"BAR")]


def test_lookup_tlsa_record(
    caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch, tmpdir_factory: pytest.TempdirFactory
) -> None:
    """Test the lookup_tlsa_record() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_2_responses)
    monkeypatch.setattr(dns.resolver.Resolver, "query", mock_tlsa_query_2_responses)
    responses = certgrinder.lookup_tlsa_record(domain="smtp.example.com", port=587, protocol="tcp")
    assert responses is not None
    assert (
        "Looking up TLSA record in DNS using system resolver: _587._tcp.smtp.example.com - all TLSA types"
        in caplog.text
    ), "Expected output not found"
    assert "Found TLSA record type 3 1 0" not in caplog.text, "TLSA 3 1 0 found in output"
    assert "Found TLSA record type 3 1 1" in caplog.text, "TLSA 3 1 1 not found in output"
    assert "Found TLSA record type 3 1 2" in caplog.text, "TLSA 3 1 2 not found in output"
    assert "Returning 2 TLSA records" in caplog.text
    assert len(responses) == 2
    caplog.clear()

    responses = certgrinder.lookup_tlsa_record(
        domain="smtp.example.com",
        port=587,
        protocol="tcp",
        tlsatype="310",
        nameserver="192.0.2.53",
    )
    assert (
        "Looking up TLSA record in DNS using configured DNS server 192.0.2.53: _587._tcp.smtp.example.com - TLSA type 3 1 0"
        in caplog.text
    ), "Expected output not found"
    assert "2 TLSA records found, but none of the type 310 were found" in caplog.text, "Expected output not found"


def mock_tlsa_query_nxdomain(*args: Any, **kwargs: Any) -> None:
    """Mock a NXDOMAIN response."""
    raise dns.resolver.NXDOMAIN


def mock_tlsa_query_noanswer(*args: Any, **kwargs: Any) -> None:
    """Mock a NoAnswer response."""
    raise dns.resolver.NoAnswer


def mock_tlsa_query_timeout(*args: Any, **kwargs: Any) -> None:
    """Mock a Timeout response."""
    raise dns.exception.Timeout


def mock_tlsa_query_exception(*args: Any, **kwargs: Any) -> None:
    """Mock an unknown exception."""
    raise Exception("Some other exception")  # noqa: TRY002,TRY003


def test_lookup_tlsa_record_exceptions(
    caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch, tmpdir_factory: pytest.TempdirFactory
) -> None:
    """Test exception responses in the lookup_tlsa_record() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_nxdomain)
    certgrinder.lookup_tlsa_record(domain="smtp.example.com", port=587, protocol="tcp")
    assert (
        "NXDOMAIN returned by system resolver, no TLSA records found in DNS for: _587._tcp.smtp.example.com"
        in caplog.text
    ), "Expected output not found for NXDOMAIN"
    caplog.clear()

    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_noanswer)
    certgrinder.lookup_tlsa_record(domain="smtp.example.com", port=587, protocol="tcp")
    assert (
        "Empty answer returned by system resolver. No TLSA records found in DNS for: _587._tcp.smtp.example.com"
        in caplog.text
    ), "Expected output not found for NoAnswer"
    caplog.clear()

    with pytest.raises(SystemExit):
        certgrinder.lookup_tlsa_record(
            domain="smtp.example.com",
            port=587,
            protocol="tcp",
            nameserver="ns.example.com",
        )
    assert (
        "Error parsing DNS server 'ns.example.com'. Only IP addresses and https URLs are supported." in caplog.text
    ), "Expected output not found for ValueError"
    caplog.clear()

    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_timeout)
    with pytest.raises(SystemExit):
        certgrinder.lookup_tlsa_record(domain="smtp.example.com", port=587, protocol="tcp")
    assert "Timeout while waiting for system resolver. Error." in caplog.text, "Expected output not found for timeout"
    caplog.clear()

    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_exception)
    certgrinder.lookup_tlsa_record(domain="smtp.example.com", port=587, protocol="tcp")
    assert "Exception <class 'Exception'> received during DNS lookup" in caplog.text, (
        "Expected output not found for other exception"
    )


def test_output_tlsa_record(
    caplog: pytest.LogCaptureFixture,
    tmpdir_factory: pytest.TempdirFactory,
    known_public_key: RSAPublicKey,
) -> None:
    """Test the output_tlsa_record() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    public_key_der_bytes = known_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    certgrinder.output_tlsa_record(
        derkey=public_key_der_bytes,
        domain="smtp.example.com",
        port=587,
        protocol="tcp",
        tlsatype="310",
        warning=True,
    )
    assert (
        "_587._tcp.smtp.example.com TLSA 3 1 0 30820222300D06092A864886F70D01010105000382020F003082020A0282020100B7385B728CCD6234B579EE7918329DA988DEB18B83EA7C45422B8281F53682AC57C93AC428EB3BFF216926662CC69D34FC2D8EE44673C9C87EF8DCDFFDE93FC5F483834465F075376691DA46FB157B68E3D58E16B5A5C0FAF026A6EAADC1FD47E55C0B2E98669CD13A9A42AFC7180F88769E409A46029CCE0FE3184A66FF3A1ABBB848CF7064EF299246CA42175EFBD30FA2A2437B19EFC9DA7BCAFA74D583DA8397B84B3492E7C084AA31B49CF3CDE1A661F0B112F2676F1BA6C9EB9EB42EB104EE7F0C0859D9F0C3C5821602B7D628C2E62195D2174CEAABAA2794DAEBA0EB7C165A2B6EA146CEACA08EC0534DDBF74149C694B6D03EC8CAC8251215853B4171588C5B3D8B5BB4B9C9960F75B540A61759F44474648ACF9810ABA65519379030639769EECC782EF1D0B81E956839B23B77A753868625B6648E5E0ACFD31F40EDB7B26CB5D9EAB91FECDEB9EFEF5752F4F5E9A92C87B9D20732D13FE9077ABD5767065756C01B5264722BB2740AF5A1EE2A60B08C5814C8CED874DBCE2F034A364BC59473BCB65B6463DE3E6657C6B287B02050A005D74C4617735C27B324FAE004491BB646302940BB7239FDC997F3F5EC27CA683F1742F5C279780B32CE33D24FA11B63ED390BAC417CC1206FFF49FBCE203F9C31D9AAFA106FC7169723F00BC6A59E0142790135C131D38BF549183ECE52BC683FD42D07057BABB6259E810203010001"
        in caplog.text
    ), "expected output not found for TLSA 3 1 0 record"

    certgrinder.output_tlsa_record(
        derkey=public_key_der_bytes,
        domain="smtp.example.com",
        port=587,
        protocol="tcp",
        tlsatype="311",
        warning=True,
    )
    assert (
        "_587._tcp.smtp.example.com TLSA 3 1 1 D6F9BA311A04F711C19C459266D53561145AC1ABF403E368976AFE51B41FAE53"
        in caplog.text
    )

    certgrinder.output_tlsa_record(
        derkey=public_key_der_bytes,
        domain="smtp.example.com",
        port=587,
        protocol="tcp",
        tlsatype="312",
        warning=False,
    )
    assert (
        "_587._tcp.smtp.example.com TLSA 3 1 2 048D0D297B5E525795CEEBB87C8CD18436766CB87DE3B5E50EE9863DB3A12FB8E639878A4B03A0C23CC2253257266F9A695EA24207CEF284EB6FD45322AE809A"
        in caplog.text
    )


def mock_tlsa_query_real_response(*args: Any, **kwargs: Any) -> list[DNSResponse]:
    """Mock a TLSA response for the known_public_key."""
    return [
        DNSResponse(
            3,
            1,
            0,
            bytes.fromhex(
                "30820222300D06092A864886F70D01010105000382020F003082020A0282020100B7385B728CCD6234B579EE7918329DA988DEB18B83EA7C45422B8281F53682AC57C93AC428EB3BFF216926662CC69D34FC2D8EE44673C9C87EF8DCDFFDE93FC5F483834465F075376691DA46FB157B68E3D58E16B5A5C0FAF026A6EAADC1FD47E55C0B2E98669CD13A9A42AFC7180F88769E409A46029CCE0FE3184A66FF3A1ABBB848CF7064EF299246CA42175EFBD30FA2A2437B19EFC9DA7BCAFA74D583DA8397B84B3492E7C084AA31B49CF3CDE1A661F0B112F2676F1BA6C9EB9EB42EB104EE7F0C0859D9F0C3C5821602B7D628C2E62195D2174CEAABAA2794DAEBA0EB7C165A2B6EA146CEACA08EC0534DDBF74149C694B6D03EC8CAC8251215853B4171588C5B3D8B5BB4B9C9960F75B540A61759F44474648ACF9810ABA65519379030639769EECC782EF1D0B81E956839B23B77A753868625B6648E5E0ACFD31F40EDB7B26CB5D9EAB91FECDEB9EFEF5752F4F5E9A92C87B9D20732D13FE9077ABD5767065756C01B5264722BB2740AF5A1EE2A60B08C5814C8CED874DBCE2F034A364BC59473BCB65B6463DE3E6657C6B287B02050A005D74C4617735C27B324FAE004491BB646302940BB7239FDC997F3F5EC27CA683F1742F5C279780B32CE33D24FA11B63ED390BAC417CC1206FFF49FBCE203F9C31D9AAFA106FC7169723F00BC6A59E0142790135C131D38BF549183ECE52BC683FD42D07057BABB6259E810203010001"
            ),
        )
    ]


def mock_tlsa_query_no_response(*args: Any, **kwargs: Any) -> list[str]:
    """Mock a TLSA no response."""
    return []


def test_verify_tlsa_record(
    caplog: pytest.LogCaptureFixture,
    tmpdir_factory: pytest.TempdirFactory,
    known_public_key: RSAPublicKey,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the verify_tlsa_record() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com,www.example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
        }
    )
    public_key_der_bytes = known_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_real_response)
    certgrinder.verify_tlsa_record(
        derkey=public_key_der_bytes,
        domain="smtp.example.com",
        port=587,
        protocol="tcp",
        tlsatype="310",
    )
    assert (
        "Received DNS response for TLSA type 3 1 0: 1 answers - looking for an answer matching the public key..."
        in caplog.text
    ), "Expected output not found from verify_tlsa_record() method"
    assert (
        "TLSA record for name _587._tcp.smtp.example.com type 3 1 0 matching the local key found in DNS, good."
        in caplog.text
    ), "Expected output not found from verify_tlsa_record() method"
    caplog.clear()

    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_no_response)
    certgrinder.verify_tlsa_record(
        derkey=public_key_der_bytes,
        domain="smtp.example.com",
        port=587,
        protocol="tcp",
        tlsatype="310",
    )
    assert (
        "No TLSA records for name _587._tcp.smtp.example.com of type 3 1 0 was found in DNS. This record needs to be added:"
        in caplog.text
    ), "Expected output not found for empty response"
    caplog.clear()

    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_2_responses)
    certgrinder.verify_tlsa_record(
        derkey=public_key_der_bytes,
        domain="smtp.example.com",
        port=587,
        protocol="tcp",
        tlsatype="311",
    )
    assert (
        "None of the TLSA records found in DNS for the name _587._tcp.smtp.example.com and type 311 match the local key. This record needs to be added to the DNS:"
        in caplog.text
    ), "Expected output not found for wrong tlsa type response"


def test_show_tlsa(caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory) -> None:
    """Test the show_tlsa() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
            "tlsa-port": 587,
            "tlsa-protocol": "tcp",
        }
    )
    certgrinder.load_domainset(certgrinder.conf.domain_list[0].split(","), keytype="ecdsa")
    derkey = certgrinder.keypair.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    tlsa310 = binascii.hexlify(derkey).decode("ASCII").upper()
    tlsa311 = hashlib.sha256(derkey).hexdigest().upper()
    tlsa312 = hashlib.sha512(derkey).hexdigest().upper()
    certgrinder.show_tlsa()
    assert tlsa310 in caplog.text, "Expected 3 1 0 TLSA record not found in output"
    assert tlsa311 in caplog.text, "Expected 3 1 1 TLSA record not found in output"
    assert tlsa312 in caplog.text, "Expected 3 1 2 TLSA record not found in output"


def test_check_tlsa(
    caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test the check_tlsa() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
            "tlsa-port": 587,
            "tlsa-protocol": "tcp",
        }
    )
    certgrinder.load_domainset(certgrinder.conf.domain_list[0].split(","), keytype="rsa")
    derkey = certgrinder.keypair.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    tlsa310 = binascii.hexlify(derkey).decode("ASCII").upper()
    tlsa311 = hashlib.sha256(derkey).hexdigest().upper()
    tlsa312 = hashlib.sha512(derkey).hexdigest().upper()

    def mock_tlsa_query_dynamic_response(*args: Any, **kwargs: Any) -> list[DNSResponse]:
        """Return a response with the three TLSA records."""
        return [
            DNSResponse(3, 1, 0, bytes.fromhex(tlsa310)),
            DNSResponse(3, 1, 1, bytes.fromhex(tlsa311)),
            DNSResponse(3, 1, 2, bytes.fromhex(tlsa312)),
        ]

    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_dynamic_response)
    certgrinder.check_tlsa()
    assert (
        "TLSA record for name _587._tcp.example.com type 3 1 0 matching the local key found in DNS, good."
        in caplog.text
    ), "Expected 3 1 0 output not found in output"
    assert (
        "TLSA record for name _587._tcp.example.com type 3 1 1 matching the local key found in DNS, good."
        in caplog.text
    ), "Expected 3 1 1 output not found in output"
    assert (
        "TLSA record for name _587._tcp.example.com type 3 1 2 matching the local key found in DNS, good."
        in caplog.text
    ), "Expected 3 1 2 output not found in output"
    assert certgrinder.error is False, "self.error should not be False here"
    caplog.clear()

    monkeypatch.setattr(dns.resolver, "query", mock_tlsa_query_2_responses)
    certgrinder.check_tlsa()
    assert "Problem discovered in check mode, setting self.error=True" in caplog.text, (
        "Expected self.error output not found"
    )
    assert certgrinder.error is True, "self.error should be True here"


def test_exit_1_in_check_mode(
    caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Make sure we get a systemexit with exit code 1 when self.error is True in check mode."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.error = True

    class FakeArgs(NamedTuple):
        command: str
        method: str

    args = FakeArgs(command="check", method="check_foo")
    with pytest.raises(SystemExit) as e:
        certgrinder.grind(args=args)  # type: ignore[arg-type]
    assert e.value.code == 1, "Exit code not 1 as expected"
    assert "Running in check mode and one or more errors were encountered, exit code 1" in caplog.text, (
        "Expected error text not found"
    )


def test_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the help command."""
    with pytest.raises(SystemExit) as e:
        main(["help"])
    assert e.type is SystemExit
    captured = capsys.readouterr()
    assert "ReadTheDocs" in captured.out


def test_show_configuration(capsys: pytest.CaptureFixture[str], tmpdir_factory: pytest.TempdirFactory) -> None:
    """Test the show configuration command."""
    with pytest.raises(SystemExit) as e:
        main(
            [
                "--path",
                str(tmpdir_factory.mktemp("certificates")),
                "--domain-list",
                "example.com",
                "--certgrinderd",
                "foobarbaz",
                "show",
                "configuration",
            ]
        )
    assert e.type is SystemExit
    captured = capsys.readouterr()
    assert "certgrinderd='foobarbaz'" in captured.out


def test_certgrinder_broken_configfile(
    tmpdir_factory: pytest.TempdirFactory, caplog: pytest.LogCaptureFixture, certgrinder_broken_yaml_configfile: Path
) -> None:
    """Test certgrinder with a broken yaml config."""
    with pytest.raises(SystemExit) as e:
        main(
            [
                "--path",
                str(tmpdir_factory.mktemp("certificates")),
                "--domain-list",
                "example.com",
                "--certgrinderd",
                "foobarbaz",
                "--config-file",
                str(certgrinder_broken_yaml_configfile),
                "show",
                "configuration",
            ]
        )
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert "Unable to parse YAML config file" in caplog.text


def mock_time_sleep(seconds: int) -> None:
    """A fake time.sleep()."""
    print(f"fake sleeping {seconds} seconds")


def mock_get_certificate_ok() -> bool:
    """A fake certgrinder.get_certificate() which just returns True."""
    print("pretending we got a certificate")
    return True


def mock_get_certificate_fail() -> bool:
    """A fake certgrinder.get_certificate() which just returns False."""
    print("pretending we didn't get a certificate")
    return False


def test_periodic(
    caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test the periodic() method."""
    caplog.set_level(logging.DEBUG)
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
            "periodic-sleep-minutes": 30,
        }
    )
    certgrinder.load_domainset(certgrinder.conf.domain_list[0].split(","), keytype="rsa")
    monkeypatch.setattr(time, "sleep", mock_time_sleep)

    monkeypatch.setattr(certgrinder, "get_certificate", mock_get_certificate_ok)
    result = certgrinder.periodic()
    assert result is True, "periodic() did not return True as expected"

    monkeypatch.setattr(certgrinder, "get_certificate", mock_get_certificate_fail)
    result = certgrinder.periodic()
    assert result is False, "periodic() did not return False as expected"


def test_init(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the init() function calls main() only when __name__ is __main__."""
    certgrinder.certgrinder.init()
    monkeypatch.setattr(certgrinder.certgrinder, "__name__", "__main__")
    with pytest.raises(SystemExit):
        certgrinder.certgrinder.init()


def test_run_certgrinderd_unparseable_output(
    tmpdir_factory: pytest.TempdirFactory, caplog: pytest.LogCaptureFixture, certgrinderd_broken_yaml_configfile: Path
) -> None:
    """Test run_certgrinderd() with unparseable certgrinderd output."""
    parser, args = parse_args(
        [
            "--path",
            str(tmpdir_factory.mktemp("certificates")),
            "--domain-list",
            "example.com,www.example.com",
            "show",
            "certificate",
        ]
    )
    config = copy.deepcopy(vars(args))
    config = delete_argparse_keys(config)
    certgrinder = Certgrinder()
    certgrinder.configure(userconfig=config)
    assert (
        certgrinder.run_certgrinderd(
            stdin=b"",
            command=["get", "certificate"],
            certgrinderd_stdout=b"stdout here",
            certgrinderd_stderr=b"hello\nworld",
        )
        == b"stdout here"
    ), "did not get expected output from run_certgrinderd()"
    assert "hello" in caplog.text
    assert "world" in caplog.text


def test_show_paths(caplog: pytest.LogCaptureFixture, tmpdir_factory: pytest.TempdirFactory) -> None:
    """Test the 'show paths' subcommand."""
    # paths are output at level INFO
    caplog.set_level(logging.INFO)
    parser, args = parse_args(
        [
            "--certgrinderd",
            "true",
            "--path",
            str(tmpdir_factory.mktemp("certificates")),
            "--domain-list",
            "example.com,www.example.com",
            "show",
            "paths",
        ]
    )
    config = copy.deepcopy(vars(args))
    config = delete_argparse_keys(config)
    certgrinder = Certgrinder()
    certgrinder.configure(userconfig=config)
    with pytest.raises(SystemExit) as e:
        certgrinder.grind(args)
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert str(certgrinder.keypair_path) in caplog.text
    assert str(certgrinder.csr_path) in caplog.text
    assert str(certgrinder.certificate_path) in caplog.text
    assert str(certgrinder.certificate_chain_path) in caplog.text
    assert str(certgrinder.issuer_path) in caplog.text
    assert str(certgrinder.concat_path) in caplog.text


def test_check_connection(
    certgrinderd_configfile: tuple[str, Path],
    certgrinderd_env: None,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    """Test the 'check connection' subcommand."""
    if certgrinderd_configfile[0] != "dns":
        # we only need to test this once
        return

    caplog.set_level(logging.DEBUG)
    mockargs = [
        "--path",
        str(tmpdir_factory.mktemp("certificates")),
        "--domain-list",
        "example.com,www.example.com",
        "--certgrinderd",
        f"server/certgrinderd/certgrinderd.py --config-file {certgrinderd_configfile[1]} --acme-server-url https://127.0.0.1:14000/dir",
        "--debug",
    ]
    with pytest.raises(SystemExit) as e:
        main([*mockargs, "check", "connection"])
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert "Success! Got pong response from certgrinderd" in caplog.text

    caplog.clear()
    mockargs = [
        "--path",
        str(tmpdir_factory.mktemp("certificates")),
        "--domain-list",
        "example.com,www.example.com",
        "--certgrinderd",
        "true",
        "--debug",
    ]
    with pytest.raises(SystemExit) as e:
        main([*mockargs, "check", "connection"])
    assert e.type is SystemExit, f"Exit was not as expected, it was {e.type}"
    assert e.value.code == 1, "Exit code not 1 as expected with no pong response"
    assert "Did not get a pong response in stdout from certgrinderd" in caplog.text


def test_post_renew_hooks_dir_without_runner(
    tmpdir_factory: pytest.TempdirFactory, caplog: pytest.LogCaptureFixture
) -> None:
    """Test the check_certificate_issuer() method with an empty invalid_ca_cn_list."""
    caplog.set_level(logging.DEBUG)

    # write mock hooks to hook dir
    hookdir = Path(tmpdir_factory.mktemp("hooks"))
    with (hookdir / "hooktrue").open("w") as f:
        f.write("#!/bin/sh\n/bin/true\n")
    (hookdir / "hooktrue").chmod(0o0755)
    with (hookdir / "hookfalse").open("w") as f:
        f.write("#!/bin/sh\n/bin/false\n")
    (hookdir / "hookfalse").chmod(0o0755)

    certgrinder = Certgrinder()
    certgrinder.conf.post_renew_hooks_dir = hookdir
    certgrinder.run_post_renew_hooks()

    assert "ended with exit code 0, good. Hook runtime was" in caplog.text
    assert "Got exit code 1 when running post_renew_hook" in caplog.text


def test_load_certificates_broken_input(tmpdir_factory: pytest.TempdirFactory) -> None:
    """Test the load_certificates() method with some broken input."""
    certgrinder = Certgrinder()
    certgrinder.configure(
        userconfig={
            "path": str(tmpdir_factory.mktemp("certificates")),
            "domain-list": ["example.com"],
            "certgrinderd": "true",
            "log-level": "DEBUG",
            "staging": True,
        }
    )
    certgrinder.load_domainset(certgrinder.conf.domain_list[0].split(","), keytype="rsa")
    path = tmpdir_factory.mktemp("fakecert") / "not_a_PEM.pem"
    with path.open("w") as f:
        f.write(
            """-----BEGIN CERTIFICATE-----
NOT_A_PEM
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
ALSO_NOT_A_PEM
-----END CERTIFICATE-----"""
        )

    certgrinder.load_certificates(path)


def test_certgrinderd_show_acmeaccount_command(
    certgrinderd_env: None, certgrinderd_configfile: tuple[str, Path]
) -> None:
    """Test calling certgrinderd with the 'show acmeaccount' subcommand."""
    if certgrinderd_configfile[0] != "dns":
        # we only need to test this once
        return

    p = subprocess.Popen(
        [
            "server/certgrinderd/certgrinderd.py",
            "--debug",
            "--config-file",
            certgrinderd_configfile[1],
            "show",
            "acmeaccount",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    certgrinderd_stdout, certgrinderd_stderr = p.communicate()
    assert p.returncode == 1
    assert (
        "Could not find an existing account for server https://acme-v02.api.letsencrypt.org/directory"
        in certgrinderd_stderr.decode()
    )
