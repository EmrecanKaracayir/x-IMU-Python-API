from enum import Enum
from .Quaternion import *

class ErrorCode(Enum):
    ERR_MORE_THAN_1_BYTE_FOR_NEW_BYTE = -2
    ERR_PACKET_HEADER_UNDEFINED = -1
    ERR_NO_ERROR = 0
    ERR_INVALID_NUM_BYTES_FOR_PACKET_HEADER = 12

class PacketHeaders(Enum):
    PKT_QUATERNION_DATA = 10

class PacketLengths(Enum):
    LEN_QUATERNION_DATA = 10

class FixedQ(Enum):
    Q_QUATERNION = 15

class XimuReceiver():
    __buffer = bytearray(256)
    __bufferIndex = 0

    isQueternionReady = False
    __queternion: Queternion

    def processNewByte(self, b: bytes):
        if len(b) > 1:
            return ErrorCode.ERR_MORE_THAN_1_BYTE_FOR_NEW_BYTE
        
        self.__buffer[self.__bufferIndex] = b[0]

        # Process receive buffer if framing char received
        if b[0] & 0x80:
            # Calculate packet size
            packetSize = self.__bufferIndex - 1 - ((self.__bufferIndex - 1) >> 3)
            self.__bufferIndex = 0
            
            # Extract packet (truncate to discard all msb)
            packet = bytearray(packetSize)
            packet[0]  = (self.__buffer[0 ] << 1) | (self.__buffer[1 ] >> 6)
            packet[1]  = (self.__buffer[1 ] << 2) | (self.__buffer[2 ] >> 5)
            packet[2]  = (self.__buffer[2 ] << 3) | (self.__buffer[3 ] >> 4)
            packet[3]  = (self.__buffer[3 ] << 4) | (self.__buffer[4 ] >> 3)
            packet[4]  = (self.__buffer[4 ] << 5) | (self.__buffer[5 ] >> 2)
            packet[5]  = (self.__buffer[5 ] << 6) | (self.__buffer[6 ] >> 1)
            packet[6]  = (self.__buffer[6 ] << 7) | (self.__buffer[7 ] >> 0)
            packet[7]  = (self.__buffer[8 ] << 1) | (self.__buffer[9 ] >> 6)
            packet[8]  = (self.__buffer[9 ] << 2) | (self.__buffer[10] >> 5)
            packet[9]  = (self.__buffer[10] << 3) | (self.__buffer[11] >> 4)
            packet[10] = (self.__buffer[11] << 4) | (self.__buffer[12] >> 3)
            packet[11] = (self.__buffer[12] << 5) | (self.__buffer[13] >> 2)
            packet[12] = (self.__buffer[13] << 6) | (self.__buffer[14] >> 1)
            packet[13] = (self.__buffer[14] << 7) | (self.__buffer[15] >> 0)
            packet[14] = (self.__buffer[16] << 1) | (self.__buffer[17] >> 6)
            packet[15] = (self.__buffer[17] << 2) | (self.__buffer[18] >> 5)
            packet[16] = (self.__buffer[18] << 3) | (self.__buffer[19] >> 4)
            packet[17] = (self.__buffer[19] << 4) | (self.__buffer[20] >> 3)
            packet[18] = (self.__buffer[20] << 5) | (self.__buffer[21] >> 2)
            packet[19] = (self.__buffer[21] << 6) | (self.__buffer[22] >> 1)
            packet[20] = (self.__buffer[22] << 7) | (self.__buffer[23] >> 0)
            packet[21] = (self.__buffer[24] << 1) | (self.__buffer[25] >> 6)
            packet[22] = (self.__buffer[25] << 2) | (self.__buffer[26] >> 5)
            packet[23] = (self.__buffer[26] << 3) | (self.__buffer[27] >> 4)
            packet[24] = (self.__buffer[27] << 4) | (self.__buffer[28] >> 3)
            packet[25] = (self.__buffer[28] << 5) | (self.__buffer[29] >> 2)
            packet[26] = (self.__buffer[29] << 6) | (self.__buffer[30] >> 1)
            packet[27] = (self.__buffer[30] << 7) | (self.__buffer[31] >> 0)

            # Interpret packet according to header
            match packet[0]:
                case PacketHeaders.PKT_QUATERNION_DATA:
                    if packetSize != PacketLengths.LEN_QUATERNION_DATA:
                        return ErrorCode.ERR_INVALID_NUM_BYTES_FOR_PACKET_HEADER
                    self.quaternionPacketHandler(packet)
                case _: 
                    return ErrorCode.ERR_PACKET_HEADER_UNDEFINED

    def quaternionPacketHandler(self, packet: bytearray):
        self.__queternion = Queternion(
            w = XimuReceiver.fixedToFloat(XimuReceiver.concat(packet[1].to_bytes(), packet[2].to_bytes()), FixedQ.Q_QUATERNION),
            x = XimuReceiver.fixedToFloat(XimuReceiver.concat(packet[3].to_bytes(), packet[4].to_bytes()), FixedQ.Q_QUATERNION),
            y = XimuReceiver.fixedToFloat(XimuReceiver.concat(packet[5].to_bytes(), packet[6].to_bytes()), FixedQ.Q_QUATERNION),
            z = XimuReceiver.fixedToFloat(XimuReceiver.concat(packet[7].to_bytes(), packet[8].to_bytes()), FixedQ.Q_QUATERNION)
        )
        self.isQueternionReady = True
    
    @staticmethod
    def fixedToFloat(fixed: bytes, q: FixedQ) -> float:
        return fixed[0] / (1 << q.value)
    
    @staticmethod
    def concat(msb: bytes, lsb: bytes) -> bytes:
        return ((msb[0] << 8) | lsb[0]).to_bytes()
    
    def getQuaternion(self):
        if (self.isQueternionReady):
            self.isQueternionReady = False
            return self.__queternion