/**
 * @file std_msgs.h
 * @brief Basic standard message types for RTOS CLI topics (float, int, bool, string).
 *
 * This header defines the most commonly used message structures in FreeRTOS-based projects.
 * All messages include a timestamp to facilitate temporal coherence in distributed systems.
 */

#ifndef STD_MSGS_H
#define STD_MSGS_H

#include <Arduino.h>
#include <stdint.h>

namespace std_msgs {

    /**
     * @brief Float message
     */
    struct Float32 {
        uint32_t timestamp;  ///< Timestamp in milliseconds
        float data;          ///< Floating point value
    };

    /**
     * @brief Integer message
     */
    struct Int32 {
        uint32_t timestamp;  ///< Timestamp in milliseconds
        int32_t data;        ///< 32-bit signed integer
    };

    /**
     * @brief Boolean message
     */
    struct Bool {
        uint32_t timestamp;  ///< Timestamp in milliseconds
        bool data;           ///< Boolean value
    };

    /**
     * @brief String message
     */
    struct StringMsg {
        uint32_t timestamp;  ///< Timestamp in milliseconds
        String data;         ///< String value
    };

} // namespace std_msgs

#endif // STD_MSGS_H
