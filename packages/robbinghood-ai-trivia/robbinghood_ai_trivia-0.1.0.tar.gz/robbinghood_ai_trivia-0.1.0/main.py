import os
import argparse
from config import Config
from camera.camera_manager import CameraManager
from ocr.ocr_processor import OCRProcessor
from ui.display import DisplayManager
from core.app import RobbinHoodApp

def main():
    """Main entry point for the RobbinHood application"""
    parser = argparse.ArgumentParser(description="RobbingHood AI Trivia Assistant")
    parser.add_argument("--list_cameras", action="store_true", help="List available cameras and exit.")
    parser.add_argument("--camera_index", type=int, default=None, help="Index of the camera to use.")
    parser.add_argument("--mode", type=str, default="gui", choices=["gui", "cli"], help="Run in GUI or CLI (single-shot) mode. Default is gui.")
    parser.add_argument("--ai_models", type=str, default="sonar_pro", help="Comma-separated list of AI models to use in CLI mode (e.g., gpt4,sonar_pro,sonar). Default is sonar_pro.")
    
    args = parser.parse_args()

    # First, initialize config and validate credentials
    try:
        config = Config()
    except ValueError as e:
        # This is likely a credential error, so print the full detailed message
        print(f"{e}")
        return 1
    except Exception as e:
        print(f"Unexpected error during configuration: {e}")
        return 1
    
    # Once credentials are validated, proceed with camera initialization
    try:
        # Get available cameras
        available_cameras = CameraManager.list_available_cameras()
        if not available_cameras:
            print("No cameras detected. Ensure your camera is connected and permissions are granted.")
            return 1
        
        if args.list_cameras:
            print("\nAvailable cameras:")
            for i, (idx, name) in enumerate(available_cameras):
                print(f"{i+1}. Index: {idx}, Name: {name}")
            return 0

        camera_index = 0 # defaults to first cam
        camera_name = None
        # listing out the cameras 
        if args.camera_index is not None:
            found_camera = False
            for idx, name in available_cameras:
                if idx == args.camera_index:
                    camera_index = idx
                    camera_name = name
                    found_camera = True
                    break
            if not found_camera:
                print(f"Camera with index {args.camera_index} not found. Using default camera.")
                # Default to the first camera if specified index is not found
                camera_index, camera_name = available_cameras[0]
        elif len(available_cameras) > 1:
            print("\nAvailable cameras:")
            for i, (idx, name) in enumerate(available_cameras):
                print(f"{i+1}. {name} (Index: {idx})")
            
            try:
                selection = int(input(f"Select camera (1-{len(available_cameras)}): "))
                if 1 <= selection <= len(available_cameras):
                    camera_index, camera_name = available_cameras[selection-1]
                else:
                    # Default to the first camera if selection is invalid
                    camera_index, camera_name = available_cameras[0]
                    print(f"Invalid selection. Using {camera_name}.")
            except ValueError:
                # Default to the first camera if input is not a number
                camera_index, camera_name = available_cameras[0]
                print(f"Invalid input. Using {camera_name}.")
        else:
            # If only one camera or no specific index is provided, use the first one
            camera_index, camera_name = available_cameras[0]
        
        camera_manager = CameraManager(camera_index, camera_name)
        print(f"Using {camera_name}")
        
        ocr_processor = OCRProcessor(config.vision_client)
        
        if args.mode == "cli":
            app = RobbinHoodApp(config, camera_manager, ocr_processor) # No DisplayManager for CLI
            ai_model_keys = [model.strip() for model in args.ai_models.split(',') if model.strip()]
            if not ai_model_keys:
                ai_model_keys = ["sonar_pro"] # Default if empty or invalid input
            app.run_cli_single_shot(ai_processor_keys=ai_model_keys)
        else: # gui mode (default)
            display_manager = DisplayManager(camera_manager)
            app = RobbinHoodApp(config, camera_manager, ocr_processor, display_manager)
            app.run()
        
    except ValueError as e:
        # Handle validation errors with detailed messages
        print(f"Validation error: {e}")
        return 1
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 