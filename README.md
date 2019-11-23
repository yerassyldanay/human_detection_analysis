## Human Detection API

#### This project has been created to handle human detection process in one place

##### Input:
```json
{
      "camera_id": "<provide_camera_id>: string/int",
      "task_id": "<provide_task_id>: string/int",
      "frame": "<provide_base64>: string",
      "points": "<provide_points_of_a_line>: list",
      "frame_shape": "<provide_shapes_of_a_frame>: list"
}
```

##### Output:
```json
 {
      "camera_id": "<provide_camera_id>: string/int",
      "task_id": "<provide_task_id>: string/int",
      "is_alert": "<provide_alert_state>: boolean",
      "objects": "<provide_objects>: list of objects"
 }
```


##### Black Box requests

##### Input:
```Blackbox.receiveFrame
(
      camera_id (string),
      frame (matrix of image),
      points (list of points of crossing-line [x1, y1, x2, y2])
 )
```

##### Output:
```json
 {
      "is_alert": "<provide_is_alert>: boolean",
      "objects": "<provide_objects>: list of list"
 }
```


##### 'Objects' struct:
```json
 {
      "id": "<provide_id_of_object>: integer",
      "x1": "<provide_x1_of_object>: integer",
      "y1": "<provide_y1_of_object>: integer",
      "x2": "<provide_x2_of_object>: integer",
      "y2": "<provide_y2_of_object>: integer",
      "class": "<provide_class_of_object>: integer",
 }
```