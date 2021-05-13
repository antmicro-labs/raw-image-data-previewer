# raw-image-data-previewer

## Supported formats informations

### RGB-like

| Name    |     VL42 Identifier    |   current support  |   future support   |
|---------|:----------------------:|:------------------:|:------------------:|
| RGB332  | `V4L2_PIX_FMT_RGB332`  | :heavy_check_mark: | :heavy_minus_sign: |
| ARGB444 | `V4L2_PIX_FMT_ARGB444` | :heavy_check_mark: | :heavy_minus_sign: |
| RGBA444 | `V4L2_PIX_FMT_RGBA444` | :heavy_check_mark: | :heavy_minus_sign: |
| ABGR444 | `V4L2_PIX_FMT_ABGR444` | :heavy_check_mark: | :heavy_minus_sign: |
| BGRA444 | `V4L2_PIX_FMT_BGRA444` | :heavy_check_mark: | :heavy_minus_sign: |
| ARGB555 | `V4L2_PIX_FMT_ARGB555` | :heavy_check_mark: | :heavy_minus_sign: |
| RGBA555 | `V4L2_PIX_FMT_RGBA555` | :heavy_check_mark: | :heavy_minus_sign: |
| ABGR555 | `V4L2_PIX_FMT_ABGR555` | :heavy_check_mark: | :heavy_minus_sign: |
| BGRA555 | `V4L2_PIX_FMT_BGRA555` | :heavy_check_mark: | :heavy_minus_sign: |
| RGB565  | `V4L2_PIX_FMT_RGB565`  | :heavy_check_mark: | :heavy_minus_sign: |
| BGR24   | `V4L2_PIX_FMT_BGR24`   | :heavy_check_mark: | :heavy_minus_sign: |
| RGB24   | `V4L2_PIX_FMT_RGB24`   | :heavy_check_mark: | :heavy_minus_sign: |
| ABGR32  | `V4L2_PIX_FMT_ABGR32`  | :heavy_check_mark: | :heavy_minus_sign: |
| BGRA32  | `V4L2_PIX_FMT_BGRA32`  | :heavy_check_mark: | :heavy_minus_sign: |
| RGBA32  | `V4L2_PIX_FMT_RGBA32`  | :heavy_check_mark: | :heavy_minus_sign: |
| ARGB32  | `V4L2_PIX_FMT_ARGB32`  | :heavy_check_mark: | :heavy_minus_sign: |

### YUV

| Name |     VL42 Identifier    | Pixel plane |   current support  |   future support   |
|------|:----------------------:|:-----------:|:------------------:|:------------------:|
| UYVY |   `V4L2_PIX_FMT_UYVY`  |    PACKED   | :heavy_check_mark: | :heavy_minus_sign: |
| YUYV |   `V4L2_PIX_FMT_YUYV`  |    PACKED   | :heavy_check_mark: | :heavy_minus_sign: |
| VYUY |   `V4L2_PIX_FMT_VYUY`  |    PACKED   | :heavy_check_mark: | :heavy_minus_sign: |
| YVYU |   `V4L2_PIX_FMT_YVYU`  |    PACKED   | :heavy_check_mark: | :heavy_minus_sign: |
| NV12 |   `V4L2_PIX_FMT_NV12`  | SEMI-PLANAR | :heavy_check_mark: | :heavy_minus_sign: |
| NV21 |   `V4L2_PIX_FMT_NV21`  | SEMI-PLANAR | :heavy_check_mark: | :heavy_minus_sign: |
| I420 |  `V4L2_PIX_FMT_YUV420` |    PLANAR   |         :x:        | :heavy_check_mark: |
| YV12 |  `V4L2_PIX_FMT_YVU420` |    PLANAR   |         :x:        | :heavy_check_mark: |
| I422 | `V4L2_PIX_FMT_YUV422P` |    PLANAR   |         :x:        | :heavy_check_mark: |

### Bayer RGB

| Name |     VL42 Identifier    |   current support  |   future support   |
|------|:----------------------:|:------------------:|:------------------:|
| RGGB |  `V4L2_PIX_FMT_SRGGB8` | :heavy_check_mark: | :heavy_minus_sign: |
| RG10 | `V4L2_PIX_FMT_SRGGB10` | :heavy_check_mark: | :heavy_minus_sign: |
| RG12 | `V4L2_PIX_FMT_SRGGB12` | :heavy_check_mark: | :heavy_minus_sign: |
| RG16 | `V4L2_PIX_FMT_SRGGB16` | :heavy_check_mark: | :heavy_minus_sign: |

### GREYSCALE

| Name   |   VL42 Identifier   |   current support  |   future support   |
|--------|:-------------------:|:------------------:|:------------------:|
| GREY   | `V4L2_PIX_FMT_GREY` | :heavy_check_mark: | :heavy_minus_sign: |
| GREY10 |  `V4L2_PIX_FMT_Y10` | :heavy_check_mark: | :heavy_minus_sign: |
| GREY12 |  `V4L2_PIX_FMT_Y12` | :heavy_check_mark: | :heavy_minus_sign: |