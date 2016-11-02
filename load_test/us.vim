g/^\(.*PacketHeader\)\@!.*$/d
%s/^.*Tcp Model Test recv time: \(\d*\).*packet_number":"\(\d*\).*time_stamp":"\(\d*\).*/\1,\3,\2/g
%s/$/:f/g
update
