## Human Detection API

#### This project has been created to handle human detection process in one place

##### Input:
```json
{
      "camera_id": "<provide_camera_id>: string",
      "task_id": "<provide_task_id>: string",
      "image": "<provide_matrix>: ndarray",
      "points": "<provide_points_of_a_line>: list"
}
```

##### Output:
```json
 {
      "camera_id": "<provide_camera_id>",
      "task_id": "<provide_task_id>",
      "boxes_list": "<provide_boxes_list>",
      "scores": "<provide_scores>",
      "classes": "<provide_classes>"
 }
```


##### Black Box requests

##### Input:
```Blackbox.receiveFrame(
      camera_id (integer),
      frame (matrix of image),
      main_line (tuple of points of crossing-line [x1, y1, x2, y2])
 )
```

##### Output:
```json
 {
      "is_alert": "<provide_is_alert>",
      "objects": "<provide_objects>"
 }
```
