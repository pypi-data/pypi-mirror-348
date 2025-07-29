from setuptools import setup, find_packages

setup(
    name="ida-domain",
    version="0.0.1.dev7",
    author="Hex-Rays SA",
    author_email="support@hex-rays.com",
    description="IDA Domain API",
    long_description="""
# IDA Domain API
\n**⚠️ This is a dev pre-release version. APIs may change without notice and pre-release versions may be deleted at any time.**


## The IDA Domain API provides a Domain Model on top of IDA SDK

## Usage example:

```python
import ida_domain

print(f"IDA Domain usage example, version {ida_domain.VersionInfo.api_version}")

db = ida_domain.Database()
if db.open("program.exe"):

  print("Segments:")
  for s in db.segments.get_all():
    print(f"- Segment ({hex(s.start_ea)} - {hex(s.end_ea)})")

  print("Functions:")
  for f in db.functions.get_all():
    print(f"- Function {f.name}, ({hex(f.start_ea)} - {hex(f.end_ea)})")

    print(" - Basic blocks:")
    for b in db.functions.get_basic_blocks(f):
      print(f"  - Basic block ({hex(b.start_ea)} - {hex(b.end_ea)})")

    print(" - Disassembly:")
    for line in db.functions.get_disassembly(f):
      print(f"   {line}")
  db.close(False)
```
""",
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
      "Development Status :: 2 - Pre-Alpha",
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent",
      "Topic :: Software Development :: Disassemblers",
    ],
    packages=["ida_domain", "ida_domain.windows", "ida_domain.macos", "ida_domain.linux"],
    package_dir={
        "ida_domain": "ida_domain",
        "ida_domain.windows": "ida_domain/windows",
        "ida_domain.macos": "ida_domain/macos",
        "ida_domain.linux": "ida_domain/linux",
    },
    include_package_data=True,
    package_data={
        "ida_domain": ["*.py"],
        "ida_domain.windows": ["*.py", "*.pyd", "*.dll"],
        "ida_domain.macos": ["*.py", "*.so", "*.dylib"],
        "ida_domain.linux": ["*.py", "*.so"],
    },
    zip_safe=False,
)
