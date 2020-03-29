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


# service control
## restart
