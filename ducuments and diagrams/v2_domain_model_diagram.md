# Deepfake Detection System V2 - Domain Model Diagram

## System Overview
Version 2 introduces advanced TruFor model integration with pixel-level detection capabilities, enhanced UI with modal dialogs, and improved configuration management.

## Domain Model Diagram

```mermaid
classDiagram
    %% Core Application Layer
    class FastAPIApplication {
        +title: str
        +version: str
        +description: str
        +lifespan: AsyncContextManager
        +middleware: List[Middleware]
        +startup()
        +shutdown()
        +mount_static_files()
        +configure_cors()
    }

    %% Detection Service Layer
    class DetectionService {
        +detection_adapter: BaseAdapter
        +max_image_size: int
        +max_video_size: int
        +allowed_types: Set[str]
        +detect_deepfake(file: UploadFile): JSONResponse
        +validate_file(file: UploadFile): bool
        +health_check(): dict
    }

    %% Adapter Pattern - Base Interface
    class BaseAdapter {
        <<interface>>
        +detect(file_bytes: bytes, filename: str, mime_type: str): Dict[str, Any]*
    }

    %% TruFor Adapter (Primary Model)
    class TruForAdapter {
        +model_path: str
        +device: torch.device
        +model: EncoderDecoder
        +config: Config
        +_setup_device(device: str): torch.device
        +_load_model(): void
        +_preprocess_image(bytes): Tuple[Tensor, dict]
        +_postprocess_results(outputs): dict
        +_calculate_integrity_score(outputs): float
        +_generate_localization_map(outputs): np.array
        +_create_confidence_map(outputs): np.array
        +detect(file_bytes, filename, mime_type): Dict
    }

    %% ResNet Adapter (Alternative Model)
    class LocalResNetAdapter {
        +model_path: str
        +device: torch.device
        +model: ResNet50
        +transform: Compose
        +_load_model(): void
        +_setup_transforms(): void
        +_detect_image(bytes, filename): dict
        +_detect_video(bytes, filename): dict
        +_format_response(result, media_type): dict
        +detect(file_bytes, filename, mime_type): Dict
    }

    %% TruFor Core Components
    class TruForModel {
        +encoder: DualSegformer
        +decoder: MLPDecoder
        +noiseprint_extractor: NoiseNet
        +forward(x): Tuple[Tensor, Tensor, Tensor]
        +extract_features(x): Tensor
        +generate_detection_map(x): Tensor
        +generate_confidence_map(x): Tensor
    }

    class NoiseNet {
        +layers: Sequential
        +extract_noiseprint(image): Tensor
        +preprocess_image(image): Tensor
    }

    %% Configuration Management
    class ConfigManager {
        +model_type: str
        +model_path: str
        +server_config: dict
        +ui_config: dict
        +logging_config: dict
        +load_config(): dict
        +validate_config(): bool
    }

    %% Media Processing
    class MediaProcessor {
        +supported_formats: Set[str]
        +max_sizes: dict
        +validate_mime_type(mime_type: str): bool
        +validate_file_size(size: int, media_type: str): bool
        +extract_video_frames(video_bytes): List[Image]
        +preprocess_image(image_bytes): Image
    }

    %% Detection Result Domain Objects
    class DetectionResult {
        +request_id: str
        +media_type: str
        +status: str
        +score: float
        +score_scale: str
        +models: List[str]
        +reasons: List[str]
        +vendor_raw: dict
        +integrity: float
        +localization_map: Optional[List]
        +confidence_map: Optional[List]
        +noiseprint_analysis: Optional[dict]
    }

    class VisualizationData {
        +original_image: str
        +detection_heatmap: str
        +confidence_overlay: str
        +noiseprint_visualization: str
        +localization_regions: List[dict]
        +generate_heatmap(): str
        +create_overlay(): str
    }

    %% Web Frontend Components
    class WebInterface {
        +upload_component: FileUploader
        +result_display: ResultViewer
        +modal_dialog: DecisionModal
        +visualization_panel: VisualizationPanel
        +handle_file_upload(): void
        +display_results(result): void
        +show_decision_details(): void
    }

    class DecisionModal {
        +modal_element: HTMLElement
        +decision_details: HTMLElement
        +show(): void
        +hide(): void
        +populate_content(data): void
        +handle_close_events(): void
    }

    class VisualizationPanel {
        +canvas_container: HTMLElement
        +original_display: HTMLElement
        +heatmap_display: HTMLElement
        +confidence_display: HTMLElement
        +render_original(image): void
        +render_heatmap(data): void
        +render_confidence_map(data): void
        +create_interactive_overlay(): void
    }

    %% Model Management
    class ModelManager {
        +available_models: dict
        +active_model: str
        +model_cache: dict
        +load_model(model_type: str): BaseAdapter
        +switch_model(model_type: str): void
        +validate_model_files(): bool
        +download_models(): void
    }

    %% Relationships
    FastAPIApplication ||--|| DetectionService : contains
    DetectionService ||--|| BaseAdapter : uses
    BaseAdapter <|-- TruForAdapter : implements
    BaseAdapter <|-- LocalResNetAdapter : implements
    
    TruForAdapter ||--|| TruForModel : uses
    TruForAdapter ||--|| ConfigManager : uses
    TruForAdapter ||--|| MediaProcessor : uses
    
    TruForModel ||--|| NoiseNet : contains
    
    DetectionService ||--|| DetectionResult : produces
    DetectionResult ||--|| VisualizationData : contains
    
    WebInterface ||--|| DecisionModal : contains
    WebInterface ||--|| VisualizationPanel : contains
    
    FastAPIApplication ||--|| ModelManager : uses
    ModelManager ||--|| BaseAdapter : manages

    %% Notes
    note for TruForAdapter "Primary model with pixel-level\ndetection and localization"
    note for LocalResNetAdapter "Fallback model for\nfast binary classification"
    note for DecisionModal "Enhanced modal with\ncentered positioning and\ndetailed analysis display"
```

## Key Domain Concepts

### 1. **Multi-Model Architecture**
- **TruForAdapter**: Advanced forensic model with pixel-level detection
- **LocalResNetAdapter**: Fast binary classification model
- **BaseAdapter**: Common interface ensuring consistency

### 2. **Enhanced Detection Results**
- **Integrity Score**: Overall authenticity assessment
- **Localization Maps**: Pixel-level manipulation detection
- **Confidence Maps**: Reliability assessment for each region
- **Noiseprint Analysis**: Digital fingerprint analysis

### 3. **Improved User Interface**
- **Decision Modal**: Centered modal with detailed analysis
- **Visualization Panel**: Multi-layer result display
- **Interactive Elements**: Hover effects and detailed breakdowns

### 4. **Configuration Management**
- **Model Selection**: Runtime model switching capability
- **Environment Configuration**: Flexible deployment options
- **Resource Management**: Memory and GPU optimization

### 5. **Media Processing Pipeline**
- **Format Validation**: Support for images and videos
- **Size Constraints**: Configurable file size limits
- **Preprocessing**: Standardized input preparation

## Version 2 Enhancements

1. **TruFor Integration**: State-of-the-art forensic analysis
2. **Pixel-Level Detection**: Precise manipulation localization
3. **Enhanced Visualization**: Multi-layer result presentation
4. **Improved UI**: Better modal positioning and user experience
5. **Configuration System**: Centralized settings management
6. **Model Management**: Dynamic model loading and switching
7. **Error Handling**: Comprehensive error recovery
8. **Internationalization**: English translation of all components
