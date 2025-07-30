
#include "proton/codec.h"
#include "proton/condition.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


/* D.R */
size_t pn_amqp_decode_DqR(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[.....D..D.[.....RR]] */
size_t pn_amqp_decode_DqEqqqqqDqqDqEqqqqqRRee(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1);
/* D.[.....D..D.[R]...] */
size_t pn_amqp_decode_DqEqqqqqDqqDqEReqqqe(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[.....D..DL....] */
size_t pn_amqp_decode_DqEqqqqqDqqDLqqqqe(pn_bytes_t bytes, uint64_t* arg0);
/* D.[.....D.[.....R.R.RR]] */
size_t pn_amqp_decode_DqEqqqqqDqEqqqqqRqRqRRee(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2, pn_bytes_t* arg3);
/* D.[?HIII?I] */
size_t pn_amqp_decode_DqEQHIIIQIe(pn_bytes_t bytes, bool* arg0, uint16_t* arg1, uint32_t* arg2, uint32_t* arg3, uint32_t* arg4, bool* arg5, uint32_t* arg6);
/* D.[?I?L] */
size_t pn_amqp_decode_DqEQIQLe(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, bool* arg2, uint64_t* arg3);
/* D.[?IIII?I?II.o] */
size_t pn_amqp_decode_DqEQIIIIQIQIIqoe(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, uint32_t* arg2, uint32_t* arg3, uint32_t* arg4, bool* arg5, uint32_t* arg6, bool* arg7, uint32_t* arg8, uint32_t* arg9, bool* arg10);
/* D.[?S?S?I?HI..RRR] */
size_t pn_amqp_decode_DqEQSQSQIQHIqqRRRe(pn_bytes_t bytes, bool* arg0, pn_bytes_t* arg1, bool* arg2, pn_bytes_t* arg3, bool* arg4, uint32_t* arg5, bool* arg6, uint16_t* arg7, uint32_t* arg8, pn_bytes_t* arg9, pn_bytes_t* arg10, pn_bytes_t* arg11);
/* D.[?o?oR] */
size_t pn_amqp_decode_DqEQoQoRe(pn_bytes_t bytes, bool* arg0, bool* arg1, bool* arg2, bool* arg3, pn_bytes_t* arg4);
/* D.[Bz] */
size_t pn_amqp_decode_DqEBze(pn_bytes_t bytes, uint8_t* arg0, pn_bytes_t* arg1);
/* D.[D.[sSR]] */
size_t pn_amqp_decode_DqEDqEsSRee(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2);
/* D.[I?Iz.?oo.D?LRooo] */
size_t pn_amqp_decode_DqEIQIzqQooqDQLRoooe(pn_bytes_t bytes, uint32_t* arg0, bool* arg1, uint32_t* arg2, pn_bytes_t* arg3, bool* arg4, bool* arg5, bool* arg6, bool* arg7, uint64_t* arg8, pn_bytes_t* arg9, bool* arg10, bool* arg11, bool* arg12);
/* D.[IoR] */
size_t pn_amqp_decode_DqEIoRe(pn_bytes_t bytes, uint32_t* arg0, bool* arg1, pn_bytes_t* arg2);
/* D.[R] */
size_t pn_amqp_decode_DqERe(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[SIo?B?BD.[SIsIo.s]D.[SIsIo]..IL..?R] */
size_t pn_amqp_decode_DqESIoQBQBDqESIsIoqseDqESIsIoeqqILqqQRe(pn_bytes_t bytes, pn_bytes_t* arg0, uint32_t* arg1, bool* arg2, bool* arg3, uint8_t* arg4, bool* arg5, uint8_t* arg6, pn_bytes_t* arg7, uint32_t* arg8, pn_bytes_t* arg9, uint32_t* arg10, bool* arg11, pn_bytes_t* arg12, pn_bytes_t* arg13, uint32_t* arg14, pn_bytes_t* arg15, uint32_t* arg16, bool* arg17, uint32_t* arg18, uint64_t* arg19, bool* arg20, pn_bytes_t* arg21);
/* D.[azSSSassttSIS] */
size_t pn_amqp_decode_DqEazSSSassttSISe(pn_bytes_t bytes, pn_atom_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2, pn_bytes_t* arg3, pn_bytes_t* arg4, pn_atom_t* arg5, pn_bytes_t* arg6, pn_bytes_t* arg7, pn_timestamp_t* arg8, pn_timestamp_t* arg9, pn_bytes_t* arg10, uint32_t* arg11, pn_bytes_t* arg12);
/* D.[o?BIoI] */
size_t pn_amqp_decode_DqEoQBIoIe(pn_bytes_t bytes, bool* arg0, bool* arg1, uint8_t* arg2, uint32_t* arg3, bool* arg4, uint32_t* arg5);
/* D.[oI?IoR] */
size_t pn_amqp_decode_DqEoIQIoRe(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, bool* arg2, uint32_t* arg3, bool* arg4, pn_bytes_t* arg5);
/* D.[sSR] */
size_t pn_amqp_decode_DqEsSRe(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2);
/* D.[s] */
size_t pn_amqp_decode_DqEse(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[sz] */
size_t pn_amqp_decode_DqEsze(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1);
/* D.[z] */
size_t pn_amqp_decode_DqEze(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D?L. */
size_t pn_amqp_decode_DQLq(pn_bytes_t bytes, bool* arg0, uint64_t* arg1);
/* D?L?. */
size_t pn_amqp_decode_DQLQq(pn_bytes_t bytes, bool* arg0, uint64_t* arg1, bool* arg2);
/* R */
size_t pn_amqp_decode_R(pn_bytes_t bytes, pn_bytes_t* arg0);
