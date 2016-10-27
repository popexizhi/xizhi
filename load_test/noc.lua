do
	--[[
	Proto.new(name, desc)
		name: displayed in the column of “Protocol” in the packet list
		desc: displayed as the dissection tree root in the packet details
	--]]
	local PROTO_NOC = Proto("NOC-Relay", "NOC-Relay")

	local msg_types = {
        [0] = "NOC_RELAY_MSG_QUERY_HOST_REQ", --RelayQueryHostRequest
        [1] = "RelayQueryConnectionResponse",
        [2] = "RelayRegisterRequest",
        [3] = "RelayRegisterResponse",
        [4] = "RelayMsgConnectionRequest",
        [5] = "RelayMsgConnectionResponse",
        [6] = "RelayDataIndication",
        [7] = "RelayDeregisterRequest",
        [8] = "ProvisionAddHostRequest",        --NOC_RELAY_MSG_ADD_HOST_REQ de-registration request from provision server to relay        
        [9] = "ProvisionAddHostResponse",       --NOC_RELAY_MSG_ADD_HOST_RESP de-registration response, from relay to provision server
        [10] = "RelayEchoResponse",
        [11] = "Reserved_1",
        [12] = "Reserved_2",
        [13] = "Reserved_3",
        [14] = "Reserved_4",
        [22] = "NOC_RELAY_MSG_CONTROL_INDICATION" --control indication between gateway and relay, like setting up L2 connection and queue status
     }

	local results = {
        [0] = "NOC_RELAY_REGI_SUCCESS",
        [1] = "NOC_RELAY_REGI_DENIED",
     }

	--[[
	Message Header
	--]]

	-- version (1 byte)
	local f_noc_version = ProtoField.uint8("NOC.Version", "Version", base.DEC)
	-- message type (1 byte)
	local f_noc_msg_type = ProtoField.uint8("NOC.MsgType", "Message Type", base.DEC, msg_types)
	-- length(2 bytes)
	local f_noc_length = ProtoField.uint16("NOC.Length", "Length", base.DEC)
	-- target host id (4 bytes)
	local f_noc_target_host_id = ProtoField.uint32("NOC.TargetHostID", "Target Host ID", base.HEX)
	-- host id (4 bytes)
	local f_noc_host_id = ProtoField.uint32("NOC.HostID", "Host ID", base.HEX)
	-- connection id (8 bytes)
	local f_noc_connection_id = ProtoField.uint64("NOC.ConnectionID", "Connection ID", base.HEX)
	-- result (4 bytes)
	local f_noc_result = ProtoField.uint32("NOC.Result", "Result", base.DEC)
    -- add_host host_type(1 bytes) 
    local f_noc_host_type = ProtoField.uint32("NOC.HostType", "HostType", base.DEC)
    -- add_host data_type(1 bytes) 
    local f_noc_data_type = ProtoField.uint32("NOC.DataType", "DataType", base.DEC)
    -- add_host host_key_len(1 bytes) 
    local f_noc_host_key_len = ProtoField.uint32("NOC.HostKeyLen", "HostKeyLen", base.DEC)

	-- define the fields table of this dissector(as a protoField array)
	PROTO_NOC.fields = {f_noc_version, f_noc_msg_type, f_noc_length, f_noc_target_host_id, 
		f_noc_host_id, f_noc_connection_id, f_noc_result}

	--[[
	Dissector Function
	--]]
	local function noc_dissector(buf, pkt, root)
		-- check buffer length
 		local buf_len = buf:len()
        if buf_len < 4 then
            return false
        end

        -- packet list columns
        pkt.cols.protocol = "NOC-Relay"
        pkt.cols.info = "NOC-Relay"
 
        -- tree root
        local t = root:add(PROTO_NOC, buf(0,buf_len))

        -- NOC Header
        t:add(f_noc_version, buf(0,1))
        t:add(f_noc_msg_type, buf(1,1))
        t:add(f_noc_length, buf(2,2))

        -- Different message
        local msg_type = buf(1,1):uint()
        local msg_len = buf(2,2):uint()

        if msg_type == 0 then -- RelayQueryHostRequest
        	t:add(f_noc_host_id, buf(4,4))                
        	pkt.cols.info = "NOC_RELAY_MSG_QUERY_HOST_REQ"

        elseif msg_type == 1 then -- RelayQueryConnectionResponse
        	pkt.cols.info = "RelayQueryConnectionResponse"

		elseif msg_type == 2 then -- RelayRegisterRequest
			if buf_len < 8 or msg_len < 4 then 
        		return false
        	end
        	t:add(f_noc_host_id, buf(4,4))
        	pkt.cols.info = "RelayRegisterRequest"

		elseif msg_type == 3 then -- RelayRegisterResponse
			if buf_len < 8 or msg_len < 4 then 
        		return false
        	end
        	t:add(f_noc_host_id, buf(4,4))
        	pkt.cols.info = "RelayRegisterResponse"

        elseif msg_type == 4 then -- RelayMsgConnectionRequest
			if buf_len < 12 or msg_len < 8 then 
        		return false
        	end
        	t:add(f_noc_target_host_id, buf(4,4))
        	t:add(f_noc_host_id, buf(8,4))
        	pkt.cols.info = "RelayMsgConnectionRequest"

        elseif msg_type == 5 then -- RelayMsgConnectionResponse
			if buf_len < 12 or msg_len < 8 then 
        		return false
        	end
        	t:add(f_noc_target_host_id, buf(4,4))
        	t:add(f_noc_host_id, buf(8,4))
        	pkt.cols.info = "RelayMsgConnectionResponse"

        elseif msg_type == 22 then --  NOC_RELAY_MSG_CONTROL_INDICATION
			if buf_len < 12 or msg_len < 8 then 
        		return false
        	end
        	t:add(f_noc_target_host_id, buf(4,4))
        	t:add(f_noc_host_id, buf(8,4))
        	pkt.cols.info = "NOC_RELAY_MSG_CONTROL_INDICATION"

		elseif msg_type == 6 then -- RelayDataIndication
			if buf_len < 12 or msg_len < 8 then 
        		return false
        	end
        	t:add(f_noc_target_host_id, buf(4,4))
        	t:add(f_noc_host_id, buf(8,4))

        	local dissector_tables = DissectorTable.get("udp.port")
			local dissector = dissector_tables:get_dissector("443") -- QUIC port is 443
			dissector:call(buf(12):tvb(), pkt, root)

        	pkt.cols.info = "RelayDataIndication (QUIC over NOC-Relay)"
		elseif msg_type == 7 then -- RelayDeregisterRequest
			pkt.cols.info = "RelayDeregisterRequest"

		elseif msg_type == 8 then -- ProvisionAddHostRequest
        	t:add(f_noc_host_id, buf(4,4))
            --t:add(f_noc_host_type, buf(8,1))
            --t:add(f_noc_data_type, buf(9,1))
            --t:add(f_noc_host_key_len, buf(10,1))

			pkt.cols.info = "ProvisionAddHostRequest"
		elseif msg_type == 9 then -- ProvisionAddHostResponse 
            t:add(f_noc_host_id, buf(4,4))
            t:add(f_noc_result, buf(8,4))
			pkt.cols.info = "ProvisionAddHostResponse"

		elseif msg_type == 10 then -- RelayEchoResponse
			pkt.cols.info = "RelayEchoResponse"

		else
			return false
		end

		return true
	end

	--[[
	Dissect Process
	--]]
	function PROTO_NOC.dissector(buf, pkt, root)
		if noc_dissector(buf, pkt, root) then
        -- valid NOC diagram
        else
            data_dis:call(buf, pkt, root)
        end
	end

	--[[
	Specify Protocol Port
	--]]
	local tcp_encap_table = DissectorTable.get("tcp.port")
	tcp_encap_table:add(12200, PROTO_NOC) -- Xgw
    tcp_encap_table:add(12201, PROTO_NOC) -- Provision
	tcp_encap_table:add(13200, PROTO_NOC) -- Xgw_test
    tcp_encap_table:add(13201, PROTO_NOC) -- Provision_test
end
