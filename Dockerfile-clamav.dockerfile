ARG base_image
FROM ${base_image}

USER root
RUN apk add clamav
RUN freshclam

# RUN ./clamscan.sh

# https://askubuntu.com/questions/591964/clamav-cant-read-file-error
# sysfs is a virtual file system provided by the Linux kernel.
# By using virtual files, sysfs exports information about various
# kernel subsystems, hardware devices and associated device drivers
# from the kernel's device model to user space. In addition to providing
# information about various devices and kernel subsystems, exported virtual
# files are also used for their configuring.

RUN  clamscan --infected --exclude-dir="^/sys" --exclude-dir="^/proc" --exclude-dir="^/mnt" --recursive /
