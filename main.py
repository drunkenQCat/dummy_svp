import json
from models.svp import Svp
from utils.word_utils import generate_words_from_svp, update_lyric_to_doremi, update_name_to_doremi
from utils.doremi_mapping import get_doremi_from_words
import click
from click import command, argument

@command()
@argument("input_file", type=click.Path(exists=True))
def replace_lyrics(input_file: str):
    # 读取原始 svp 文件
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()
        # 去除末尾的 null 字符 '\x00'
        data = data.rstrip('\x00')
        svp_data = json.loads(data)

    # 创建 Svp 实例
    svp_instance = Svp(**svp_data)

    # 生成 Word 对象列表
    words = generate_words_from_svp(svp_instance)

    # 获取 do-re-mi 映射
    doremi_map = get_doremi_from_words(words)

    update_name_to_doremi(doremi_map, words)

    # 更新单词名称为 do-re-mi
    update_lyric_to_doremi(words)

    # 将修改后的.get(note.pitch.name, "do")
    output_file = input_file.replace(".svp", "_doremi.svp")
    with open(output_file, "w", encoding="utf-8") as f:
        json_output = svp_instance.model_dump_json()
        f.write(json_output + '\x00') 

if __name__ == "__main__":
    replace_lyrics() 