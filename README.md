## Human Detection API

#### This project has been created to handle human detection process in one place

##### Input:
```json
{
      "camera_id": "<provide_camera_id>: string",
      "tesk_id": "<provide_task_id>: string",
      "image": "<provide_matrix>: ndarray",
      "points": "<provide_points_of_a_line>: list"
}
```

##### Output:
```json
 {
      "camera_id": "<provide_camera_id>",
      "tesk_id": "<provide_task_id>",
      "boxes_list": "<provide_boxes_list>",
      "scores": "<provide_scores>",
      "classes": "<provide_classes>"
 }
```
