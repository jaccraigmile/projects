import socket
from assemblyline_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection

EICAR_STRING = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!"

class ClamAV(ServiceBase):
    def start(self):
        self.log.info("ClamAV service started")

    def execute(self, request):
        result = Result()

        host = self.config.get("CLAMAV_HOST")
        port = self.config.get("CLAMAV_PORT")

        file_path = request.file_path

        scan_result = self.scan_file(host, port, file_path)

        if scan_result["infected"]:
            section = ResultSection(
                title="ClamAV Detection",
                classification=self.classification
            )
            section.add_line(f"Malware detected: {scan_result['signature']}")
            section.set_heuristic(1)
            result.add_section(section)

            request.set_status("malicious")
        else:
            section = ResultSection(
                title="ClamAV Scan Result",
                classification=self.classification
            )
            section.add_line("No malware detected")
            result.add_section(section)

        request.result = result

    def scan_file(self, host, port, file_path):
        """
        Send INSTREAM scan to clamd
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        sock.sendall(b"zINSTREAM\0")

        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sock.sendall(len(chunk).to_bytes(4, byteorder="big") + chunk)

        sock.sendall(b"\0\0\0\0")

        response = sock.recv(4096).decode()
        sock.close()

        # Example response:
        # stream: Eicar-Test-Signature FOUND
        if "FOUND" in response:
            return {
                "infected": True,
                "signature": response.split("FOUND")[0].split(":")[-1].strip()
            }

        return {"infected": False}
