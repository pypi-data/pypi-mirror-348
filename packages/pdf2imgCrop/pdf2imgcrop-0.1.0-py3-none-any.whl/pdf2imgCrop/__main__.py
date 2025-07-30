import argparse
from .core import convert_pdf

def main():
    parser = argparse.ArgumentParser(
        description="将PDF文件转换为图片并自动裁剪空白边距",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "file",
        help="PDF文件路径,(Path to the PDF file)",
    )
    
    parser.add_argument(
        "-d", "--dpi",
        type=int,
        default=300,
        help="输出图片的DPI, 默认为 300, (DPI for output images, default is 300)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["jpg", "png"],
        default="jpg",
        help="输出图片格式, 默认为 'jpg', (Format of output images, default is 'jpg')",
    )
    
    args = parser.parse_args()
    
    try:
        convert_pdf(args.file, args.dpi, args.format)
        print(f"\n转换完成！输出目录: {args.file}output")
    except Exception as e:
        print(f"错误: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
