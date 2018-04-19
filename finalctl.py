from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  def __init__ (self, connection):
    # tracks connection to switch
    self.connection = connection
    connection.addListeners(self)

  def dst_host (self, dst):
    if dst.inNetwork("10.0.1.0/24"):
        return 1
    elif dst.inNetwork("10.0.2.0/24"):
        return 2
    elif dst.inNetwork("10.0.3.0/24"):
        return 3
    elif dst.inNetwork("10.0.4.0/24"):
        return 4
    else: return 0

  def src_host (self, src):
    if src.inNetwork("10.0.1.0/24"):
        return 1
    elif src.inNetwork("10.0.2.0/24"):
        return 2
    elif src.inNetwork("10.0.3.0/24"):
        return 3
    elif src.inNetwork("10.0.4.0/24"):
        return 4
    else: return 0

  def port_num (self, switch_id, port, src, dst):
    src_num = self.src_host(src)
    dst_num = self.dst_host(dst)
    if switch_id == 1:
        if src_num == 1:
            if dst_num == 3:
                return 10
            else: return 0
        elif src_num == 2:
            if dst_num == 4:
                return 11
            else: return 0
        elif src_num == 3:
            if dst_num == 1:
                return 8
            else: return 0
        elif src_num == 4:
            if dst_num == 2:
                return 9
            else: return 0
        else: return 0
    elif switch_id == 2:
        if (src_num == 1) or (src_num == 3):
            if dst == "10.0.1.1":
                return 8
            elif dst == "10.0.1.2":
                return 9
            elif dst_num == 3:
                return 10
            else: return 0
        else: return 0
    elif switch_id == 3:
        if (src_num == 2) or (src_num == 4):
            if dst == "10.0.2.1":
                return 8
            elif dst == "10.0.2.2":
                return 9
            elif dst_num == 4:
                return 10
            else: return 0
        else: return 0
    elif switch_id == 4:
        if (src_num == 1) or (src_num == 3):
            if dst == "10.0.3.1":
                return 8
            elif dst == "10.0.3.2":
                return 9
            elif dst_num == 1:
                return 10
            else: return 0
        else: return 0
    elif switch_id == 5:
        if (src_num == 2) or (src_num == 4):
            if dst == "10.0.4.1":
                return 8
            elif dst_num == 2:
                return 9
            else: return 0
        else: return 0

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    #port_on_switch: represents the port the packet was received on
    #switch_id represents the id of switch that received packet

    msg = of.ofp_flow_mod()
    ip = packet.find('ipv4')
    if ip:
        msg.match = of.ofp_match.from_packet(packet)
        num = self.port_num(switch_id, port_on_switch, ip.srcip, ip.dstip)
        if num != 0:
            msg.actions.append(of.ofp_action_output(port = num))
    else:
        msg.match = of.ofp_match.from_packet(packet)
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))

    msg.idle_timeout = 30
    msg.hard_timeout = 30
    msg.data = packet_in
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
