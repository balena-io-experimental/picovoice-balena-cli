import subprocess
import sys
from picovoice import Picovoice
from pvrecorder import PvRecorder
from threading import Thread
from config.intents import process_inference

recorder = None


class PicovoiceCLI(Thread):
    global network_devices

    def __init__(
        self,
        keyword_path,
        context_path,
        access_key,
        device_index,
        porcupine_sensitivity=0.75,
        rhino_sensitivity=0.25,
    ):
        super(PicovoiceCLI, self).__init__()

        def inference_callback(inference):
            return self._inference_callback(inference)

        self._picovoice = Picovoice(
            access_key=access_key,
            keyword_path=keyword_path,
            wake_word_callback=self._wake_word_callback,
            context_path=context_path,
            inference_callback=inference_callback,
            porcupine_sensitivity=porcupine_sensitivity,
            rhino_sensitivity=rhino_sensitivity,
        )

        self._context = self._picovoice.context_info

        self._device_index = device_index

    @staticmethod
    def _wake_word_callback():
        global recorder
        try:
            recorder.stop()
            subprocess.check_output(["mpg123", "-q", "listening.mp3"])
            recorder.start()

            print("[Yes?]\n")
        except subprocess.CalledProcessError as e:
            print(e)

    def _inference_callback(self, inference):
        # Print the inference result.
        print("{")
        print(
            "  is_understood : '%s',"
            % ("true" if inference.is_understood else "false")
        )
        if inference.is_understood:
            print("  intent : '%s'," % inference.intent)
            if len(inference.slots) > 0:
                print("  slots : {")
                for slot, value in inference.slots.items():
                    print("    '%s' : '%s'," % (slot, value))
                print("  }")
        print("}\n")

        # Stop the recorder to avoid hardware clash
        recorder.stop()

        try:
            # Process the inference with the users custom config
            process_inference(inference)
        except Exception as ex:
            print(ex)

        # Start the recorder again
        recorder.start()

    def run(self):
        global recorder
        try:
            recorder = PvRecorder(
                device_index=self._device_index,
                frame_length=self._picovoice.frame_length,
            )
            recorder.start()

            print(self._context)

            print("[Listening ...]")

            while True:
                pcm = recorder.read()
                self._picovoice.process(pcm)
        except KeyboardInterrupt:
            sys.stdout.write("\b" * 2)
            print("Stopping ...")
        finally:
            if recorder is not None:
                recorder.delete()

            self._picovoice.delete()
