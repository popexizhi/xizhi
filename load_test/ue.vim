g/^\(.*PacketHeader\)\@!.*$/d
%s/^.*Tcp Model Test recv time: \(\d*\).*packet_number":"\(\d*\).*time_stamp":"\(\d*\).*ue_client_\(\d*\).log.txt$/\1,\3,\4,\2/g
%s/$/:f/g
update
quit
