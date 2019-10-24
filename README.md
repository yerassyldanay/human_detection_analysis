## Human Detection API

#### This project has been created to handle human detection process in one place

##### Input:
```json
{
      "Camera_id": "<provide_camera_id>: string",
      "Task_id": "<provide_task_id>: string",
      "Frame": "<provide_base64>: string",
      "Points": "<provide_points_of_a_line>: list",
      "Frame_shape": "<provide_shapes_of_a_frame>: list"
}
```

##### Output:
```json
 {
      "Camera_id": "<provide_camera_id>: string",
      "Task_id": "<provide_task_id>: string",
      "Is_alert": "<provide_alert_state>: boolean",
      "Objects": "<provide_objects>: list of list"
 }
```


##### Black Box requests

##### Input:
```Blackbox.receiveFrame(
      Camera_id (string),
      Frame (matrix of image),
      Points (list of points of crossing-line [x1, y1, x2, y2])
 )
```

##### Output:
```json
 {
      "Is_alert": "<provide_is_alert>: boolean",
      "Objects": "<provide_objects>: list of list"
 }
```


##### 'Objects' struct:
```json
 {
      "Id": "<provide_id_of_object>: integer",
      "X1": "<provide_x1_of_object>: integer",
      "Y1": "<provide_y1_of_object>: integer",
      "X2": "<provide_x2_of_object>: integer",
      "Y2": "<provide_y2_of_object>: integer",
      "Class": "<provide_class_of_object>: integer",
 }
```