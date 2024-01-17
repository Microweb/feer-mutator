from pathlib import Path

import aiofiles


async def save_result_in_file(file_path: Path, result: str) -> None:
    async with aiofiles.open(file_path, "w") as f:
        await f.write(result)
