[Great reference](http://irq5.io/2016/12/22/raspberry-pi-zero-as-multiple-usb-gadgets/)
>    69  sudo systemctl enable getty@ttyGS0.service

# Debugging
[HID scan code](https://github.com/girst/hardpass-sendHID)
```
echo -n "hello world " | sudo ./scan /dev/hidg0 1 0 # 1 0 for
```
# HID Gadget test
https://aagallag.com/hid_gadget_test/

```
sudo hid_gadget_test /dev/hidg0 keyboard
```

journalctl -f -u myusbgadget

# more advanced
functionfs
https://www.collabora.com/news-and-blog/blog/2019/03/27/modern-usb-gadget-on-linux-and-how-to-integrate-it-with-systemd-part-2/


    load the dwc2 device tree overlay by editing config.txt,
        load the libcomposite kernel module,
            create a script that sets up the USB gadgets via ConfigFS,
                start that script at boot up using a systemd unit file.
for gt, you need to have corrent conf, otherwise gt even won't print help info.


# doc
https://www.kernel.org/doc/Documentation/ABI/testing/configfs-usb-gadget
[shell reference for take down gadget, but we can always create new ones]https://github.com/nextthingco/Gadget-OS/blob/935eaa0a35a69707f52d4f43e8e279f02cbda793/gadget/package/gadget-init-scripts/files/etc/init.d/S34_usb_gadget
# tool,lib
https://github.com/libusbgx/libusbgx

https://stackoverflow.com/questions/16188335/automake-error-no-proper-invocation-of-am-init-automake-was-found

## auto tools for making
https://stackoverflow.com/questions/26832264/confused-about-configure-script-and-makefile-in/26832773
https://www.gnu.org/software/automake/manual/html_node/Error-required-file-ltmain_002esh-not-found.html
so libtoolize first
then aclocal
then automake
./configure
make

https://wiki.archlinux.org/index.php/DocBook

# service control
## restart


