# Thursday 2020-05-29

## QR code


# due = kostnad
# iref = ocr
data = {
    "uqr": 1,
    "tp": 1,
    "nme": "dsreda DEMO",
    "cid": "123456-7890",
    "iref": "130065",
    "ddt": "20150621",
    "due": 3407.0000,
    "pt": "BG",
    "acc": "123-4567",
}


install zbar to read qrcodes with zbarimg




## CI

Problems with e2e tests, maybe x is needed for qt application to be started?
-> You can set QT to not need X in the docker image, by setting:
QT_QPA_PLATFORM=minimal
export QT_QPA_PLATFORM
make test

Found the parallell test option for coverage, -p. Pretty neat


# Thursday 2020-05-28

## CI

Lot's of problems with permissions on the virtualenvironment I tried to install
in the jenkins docker image. I gave up and will install all requirements directly
in the docker image instead.

Since there is some problem with lagging support of cgroup v2 in docker it's
easier to run podman from redhat.
