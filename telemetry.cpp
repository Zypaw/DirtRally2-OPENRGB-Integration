#include <iostream>
#include <vector>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>

const char* HOST = "0.0.0.0";
const int PORT = 20777;
const int POS_GEAR = 33;
const int POS_RPM_MAX = 63;
const int POS_RPM_CURR = 37;
const int POS_V = 7;
const int RETRY_MAX = 15;
const int BUFF_SIZE = 512;

std::map<float, char> GEAR = {
    {0.0, 'N'}, {1.0, '1'}, {2.0, '2'}, {3.0, '3'}, {4.0, '4'},
    {5.0, '5'}, {6.0, '6'}, {7.0, '7'}, {8.0, '8'}, {9.0, '9'},
    {10.0, 'R'}
};

void processTelemetry(const char* data) {
    float info[64];
    std::memcpy(info, data, 256);

    try {
        char gear = GEAR[info[POS_GEAR]];
        float power = (info[POS_RPM_CURR] * 100.0) / info[POS_RPM_MAX];
        float rpms = info[POS_RPM_CURR];
        float maxRpms = info[POS_RPM_MAX];
        float speedKmph = info[POS_V] * 3.6;

        std::cout << "GEAR: " << gear
                  << ", POWER: " << power
                  << "%, RPMS: " << rpms
                  << ", MAX_RPMS: " << maxRpms
                  << ", SPEED: " << speedKmph << " km/h\n";
    } catch (...) {
        // Handle exceptions (if any)
    }
}

int main() {
    for (int i = 0; i < RETRY_MAX; ++i) {
        try {
            int sock = socket(AF_INET, SOCK_DGRAM, 0);
            if (sock == -1) {
                throw std::runtime_error("Socket creation failed");
            }

            sockaddr_in serverAddr;
            serverAddr.sin_family = AF_INET;
            serverAddr.sin_addr.s_addr = INADDR_ANY;
            serverAddr.sin_port = htons(PORT);

            if (bind(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == -1) {
                throw std::runtime_error("Socket binding failed");
            }

            char buffer[BUFF_SIZE];
            while (true) {
                ssize_t bytesRead = recv(sock, buffer, BUFF_SIZE, 0);
                if (bytesRead > 0) {
                    processTelemetry(buffer);
                } else {
                    throw std::runtime_error("Broken socket");
                }
            }
        } catch (const std::exception& e) {
            std::cerr << e.what() << ", retry " << i << std::endl;
            sleep(1);
        }
    }

    return 0;
}