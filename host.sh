if [[ "$EUID" -ne 0 ]]; then
   echo "Please run as root";
   exit 1
fi

echo "Launching Host"

sudo qemu-system-x86_64 -smp 4 -drive format=raw,file=/home/shehbaz/sdb/40G -drive file=/dev/sdc,format=raw,if=virtio -m 4096 -enable-kvm -net user,hostfwd=tcp::10022-:22 -net nic &
sleep 20
ssh vm@localhost -p 10022
