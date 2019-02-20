while True:
 try:
 reading = ser.read().encode('hex')
     if reading =="":
         continue
 #always add to packet when it's not empty
 data_packet.append(reading)
 if check_byte == True:
 #sometimes, check byte could be 2a
 check_byte = False
 continue
 elif length_byte == True:
 #this byte is length
 packet_length = int(reading, 16)
 length_byte = False
 if packet_length == 0 and hex_equals(reading,"2a"):
 #start of a string
 #next byte is length
 length_byte = True
 elif packet_length> 0:
 packet_length -= 1
 elif hex_equals(reading,"23"):
 #end of packet
 data_packet_handle = data_packet
 data_packet = []
 handle_data(data_packet_handle)
 elif packet_length == 0:
 #if it's zero, the packet is over, but still have check and ending character
 #next byte is check byte
 check_byte = True
 except Exception, err:
 pass
 print Exception, err
