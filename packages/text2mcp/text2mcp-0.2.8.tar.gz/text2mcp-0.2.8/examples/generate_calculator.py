"""
使用text2mcp生成一个计算器MCP服务的示例
"""
from text2mcp.core.generator import CodeGenerator

def main():
    # 创建代码生成器
    generator = CodeGenerator()
    
    # 描述要生成的服务
    description = """
    创建一个计算器MCP服务，提供以下功能：
    1. 加法计算（两个数相加）
    2. 减法计算（两个数相减）
    3. 乘法计算（两个数相乘）
    4. 除法计算（两个数相除，处理除数为零的情况）
    服务应该有良好的错误处理和日志记录。
    """
    
    # 生成代码
    print("🚀 开始生成计算器MCP服务代码...")
    code = generator.generate(description)
    
    if code:
        # 保存代码到文件
        output_file = "calculator_service.py"
        path = generator.save_to_file(code, output_file, "./")
        
        if path:
            print(f"✅ 代码生成成功！已保存到: {path}")
            print("\n你可以使用以下命令运行这个服务:")
            print(f"  python {output_file}")
            print("或者使用text2mcp命令行工具:")
            print(f"  text2mcp run {output_file}")
        else:
            print("❌ 代码生成成功，但保存到文件失败")
    else:
        print("❌ 代码生成失败")

if __name__ == "__main__":
    main() 
