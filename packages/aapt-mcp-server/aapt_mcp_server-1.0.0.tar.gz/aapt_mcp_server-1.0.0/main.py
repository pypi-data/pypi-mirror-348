import os
import subprocess
import uuid
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message


aapt = FastMCP("aapt-mcp")


@aapt.tool()
def aapt_tool(
    file_path: str
) -> str:
    """
        List contents of Zip-compatible archive.
        Args:
            apk_path: a path to an apk file on local filesystem, not android device
        Returns:
            a path to a file containing the apk contents line by line.
            The output format is as follows:
            Archive:  OplusLauncher.apk
            Length   Method    Size  Ratio   Offset      Date  Time  CRC-32    Name
            --------  ------  ------- -----  -------      ----  ----  ------    ----
            10402  Stored    10402   0%         0  01-01-09 00:00  e5a33da7  assets/bar.png
            ...
            --------          -------  ---                            -------
            86865306          76165925  12%                            4863 files
    """
    # call aapt to list the contents of the apk
    aapt_output = subprocess.check_output(["aapt", "list", "-v",  file_path])

    output_file_path = f"aapt_output_{uuid.uuid4()}.txt"
    with open(output_file_path, "wb") as f:
        f.write(aapt_output)

    # get the absolute path to the file containing the apk contents
    return os.path.abspath(output_file_path)

@aapt.prompt(description="Analyze the contents of an APK file and provide insights about its size and structure.")
def analyze_table(file_path: str) -> list[Message]:
    # Read the aapt output file
    with open(file_path, 'r') as f:
        apk_contents = f.read()
    
    return [
        {
            "role": "system",
            "content": """
            You are an expert Android APK analyzer. Your task is to analyze the contents of an APK file and provide insights about its size and structure. 
            Follow these steps:
            1. Categorize files by type (resources, native libraries, dex files, etc.)
            2. Identify the largest files and directories
            3. Look for potential optimization opportunities
            4. Calculate total size and provide a breakdown
            5. Highlight any unusual patterns or potential issues
            
            Format your response as follows:
            - Total APK Size: [size]
            - Size Breakdown:
              * Resources: [size]
              * Native Libraries: [size]
              * DEX Files: [size]
              * Other: [size]
            - Top 5 Largest Files:
              1. [file path]: [size]
              2. [file path]: [size]
              ...
            - Optimization Recommendations:
              * [specific recommendation]
              * [specific recommendation]
            - Potential Issues:
              * [issue if any]
            """
        },
        {
            "role": "user",
            "content": f"Please analyze this APK contents:\n{apk_contents}"
        }
    ]

def main():
    
    aapt.run(transport="stdio")


if __name__ == "__main__":
    main()
