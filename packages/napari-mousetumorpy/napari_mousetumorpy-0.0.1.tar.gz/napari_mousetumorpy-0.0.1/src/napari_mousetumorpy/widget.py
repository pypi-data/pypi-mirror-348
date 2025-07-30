import napari.layers
from napari.qt.threading import thread_worker
from napari.utils.notifications import show_warning, show_info
from PyQt5.QtCore import Qt
from qtpy.QtWidgets import (
    QComboBox,
    QGridLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QWidget,
    QSizePolicy,
    QSpinBox,
)

from mousetumorpy import (
    LungsPredictor,
    TumorPredictor,
    NNUNET_MODELS,
    YOLO_MODELS,
    run_tracking,
    generate_tracked_tumors,
)


class TrackingWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        self.viewer = napari_viewer

        # Layout
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignTop)
        self.setLayout(grid_layout)

        # Image
        self.cb_labels = QComboBox()
        self.cb_labels.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(QLabel("Labels (4D)", self), 0, 0)
        grid_layout.addWidget(self.cb_labels, 0, 1)

        # Method
        self.cb_method = QComboBox()
        self.cb_method.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cb_method.addItems(["trackpy", "laptrack"])
        grid_layout.addWidget(QLabel("Method", self), 1, 0)
        grid_layout.addWidget(self.cb_method, 1, 1)

        # Maximum tracking distance (px)
        self.sp_max_dist = QSpinBox()
        self.sp_max_dist.setMinimum(1)
        self.sp_max_dist.setMaximum(500)
        self.sp_max_dist.setValue(30)
        self.sp_max_dist.setSingleStep(1)
        self.sp_max_dist.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(QLabel("Max dist. (px)", self), 2, 0)
        grid_layout.addWidget(self.sp_max_dist, 2, 1)

        # Run button
        self.btn = QPushButton("Run", self)
        self.btn.clicked.connect(self._run)
        grid_layout.addWidget(self.btn, 3, 0, 1, 2)

        # Progress bar
        self.pbar = QProgressBar(self, minimum=0, maximum=1)
        self.pbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(self.pbar, 4, 0, 1, 2)

        # Setup layer callbacks
        self.viewer.layers.events.inserted.connect(
            lambda e: e.value.events.name.connect(self._on_layer_change)
        )
        self.viewer.layers.events.inserted.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._on_layer_change)
        self._on_layer_change(None)

    def _on_layer_change(self, e):
        self.cb_labels.clear()
        for x in self.viewer.layers:
            if isinstance(x, napari.layers.Labels):
                if x.data.ndim == 4:
                    self.cb_labels.addItem(x.name, x.data)

    @thread_worker
    def _inference_thread(self, labels_timeseries, max_dist_px, method):
        linkage_df = run_tracking(
            tumor_timeseries=labels_timeseries,
            method=method,
            max_dist_px=max_dist_px,
            # Default parameters (Note: they could be exposed in a future version)
            image_timeseries=None,
            lungs_timeseries=None,
            with_lungs_registration=False,
            memory=0,
            dist_weight_ratio=0.9,
            max_volume_diff_rel=1.0,
            skip_level=8,
        )

        tracked_labels_timeseries = generate_tracked_tumors(labels_timeseries, linkage_df)

        return linkage_df, tracked_labels_timeseries

    def _run(self):
        selected_labels_timeseries = self.cb_labels.currentData()
        if selected_labels_timeseries is None:
            return
        
        max_dist_px = self.sp_max_dist.value()
        method = self.cb_method.currentText()

        self.pbar.setMaximum(0)

        worker = self._inference_thread(selected_labels_timeseries, max_dist_px, method)
        worker.returned.connect(self._load_in_viewer)
        worker.start()

    def _load_in_viewer(self, payload):
        """Callback from thread returning."""
        df, tracked_labels = payload

        n_tracked_tumors = len(df)

        if n_tracked_tumors == 0:
            show_warning("No tumors tracked")
        else:
            if tracked_labels is not None:
                self.viewer.add_labels(tracked_labels, name="Tracked tumors")
                show_info(f"{n_tracked_tumors} tumors tracked")
        
        self.pbar.setMaximum(1)


class LungsSegmentationWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        self.viewer = napari_viewer

        # Layout
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignTop)
        self.setLayout(grid_layout)

        # Image
        self.cb_image = QComboBox()
        self.cb_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(QLabel("Image", self), 0, 0)
        grid_layout.addWidget(self.cb_image, 0, 1)

        # Model
        self.cb_models = QComboBox()
        self.cb_models.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        for model_name in YOLO_MODELS.keys():
            self.cb_models.addItem(model_name, model_name)
        grid_layout.addWidget(QLabel("Model", self), 1, 0)
        grid_layout.addWidget(self.cb_models, 1, 1)

        # Run button
        self.btn = QPushButton("Run", self)
        self.btn.clicked.connect(self._run)
        grid_layout.addWidget(self.btn, 2, 0, 1, 2)

        # Progress bar
        self.pbar = QProgressBar(self, minimum=0, maximum=1)
        self.pbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(self.pbar, 3, 0, 1, 2)

        # Setup layer callbacks
        self.viewer.layers.events.inserted.connect(
            lambda e: e.value.events.name.connect(self._on_layer_change)
        )
        self.viewer.layers.events.inserted.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._on_layer_change)
        self._on_layer_change(None)

    def _on_layer_change(self, e):
        self.cb_image.clear()
        for x in self.viewer.layers:
            if isinstance(x, napari.layers.Image):
                if x.data.ndim in [2, 3]:
                    self.cb_image.addItem(x.name, x.data)

    @thread_worker
    def _inference_thread(self, model, image):
        predictor = LungsPredictor(model)
        roi, roi_mask = predictor.compute_3d_roi(image)
        return (roi, roi_mask)

    def _run(self):
        self.selected_image = self.cb_image.currentData()
        if self.selected_image is None:
            return

        self.selected_model = self.cb_models.currentData()
        if self.selected_model is None:
            return

        self.pbar.setMaximum(0)

        worker = self._inference_thread(self.selected_model, self.selected_image)
        worker.returned.connect(self._load_in_viewer)
        worker.start()

    def _load_in_viewer(self, payload):
        """Callback from thread returning."""
        roi, roi_mask = payload
        if roi is not None:
            self.viewer.add_image(roi, name="Image (ROI)")
        if roi_mask is not None:
            self.viewer.add_labels(roi_mask, name="Lungs (ROI)")

        self.pbar.setMaximum(1)


class TumorSegmentationWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        self.viewer = napari_viewer

        # Layout
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignTop)
        self.setLayout(grid_layout)

        # Image
        self.cb_image = QComboBox()
        self.cb_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(QLabel("Image", self), 0, 0)
        grid_layout.addWidget(self.cb_image, 0, 1)

        # Model
        self.cb_models = QComboBox()
        self.cb_models.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        for model_name in NNUNET_MODELS.keys():
            self.cb_models.addItem(model_name, model_name)
        grid_layout.addWidget(QLabel("Model", self), 1, 0)
        grid_layout.addWidget(self.cb_models, 1, 1)

        # Compute button
        self.btn = QPushButton("Run", self)
        self.btn.clicked.connect(self._run)
        grid_layout.addWidget(self.btn, 3, 0, 1, 2)

        # Progress bar
        self.pbar = QProgressBar(self, minimum=0, maximum=1)
        self.pbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(self.pbar, 4, 0, 1, 2)

        # Setup layer callbacks
        self.viewer.layers.events.inserted.connect(
            lambda e: e.value.events.name.connect(self._on_layer_change)
        )
        self.viewer.layers.events.inserted.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._on_layer_change)
        self._on_layer_change(None)

    def _on_layer_change(self, e):
        self.cb_image.clear()
        for x in self.viewer.layers:
            if isinstance(x, napari.layers.Image):
                if x.data.ndim == 3:
                    self.cb_image.addItem(x.name, x.data)

    @thread_worker
    def _inference_worker(self, model, image):
        predictor = TumorPredictor(model)
        segmentation = predictor.predict(image)
        return segmentation

    def _run(self):
        selected_image = self.cb_image.currentData()
        if selected_image is None:
            return

        selected_model = self.cb_models.currentData()
        if selected_model is None:
            return

        self.pbar.setMaximum(0)

        worker = self._inference_worker(selected_model, selected_image)
        worker.returned.connect(self._load_in_viewer)
        worker.start()

    def _load_in_viewer(self, segmentation):
        """Callback from thread returning."""
        if segmentation is not None:
            self.viewer.add_labels(segmentation, name=f"Tumors (nnUNet)")

        self.pbar.setMaximum(1)
