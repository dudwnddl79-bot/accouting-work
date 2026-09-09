#!/usr/bin/env python3
"""
ZIP에서 이미지를 추출하고 images/ 폴더에 복사하는 유틸리티.

사용법:
  python3 scripts/update_images.py --zipdir <압축해제된_폴더> --mapping scripts/image_mapping.json [--dry-run]

예시:
  python3 scripts/update_images.py --zipdir /tmp/zipcontents --mapping scripts/image_mapping.json
"""

import os
import re
import shutil
import json
import argparse


def decode_filename(s):
    """#U4F4D 형태의 URL 인코딩된 한글 파일명을 디코딩."""
    return re.sub(r'#U([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)


def list_decoded_files(zipdir):
    """zipdir 내 파일 목록을 {디코딩명: 원본인코딩명} 형태로 반환."""
    result = {}
    for fname in os.listdir(zipdir):
        decoded = decode_filename(fname)
        result[decoded] = fname
    return result


def load_mapping(mapping_file):
    """image_mapping.json 로드: {디코딩된_원본명: 타겟파일명}"""
    with open(mapping_file, encoding='utf-8') as f:
        return json.load(f)


def run(zipdir, mapping_file, images_dir, dry_run=False):
    decoded_map = list_decoded_files(zipdir)
    mapping = load_mapping(mapping_file)

    copied, missing = [], []

    for decoded_src, target in mapping.items():
        if decoded_src in decoded_map:
            src_path = os.path.join(zipdir, decoded_map[decoded_src])
            dst_path = os.path.join(images_dir, target)
            if dry_run:
                print(f"[DRY] {decoded_src} → {target}")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"OK  {decoded_src} → {target}")
            copied.append(target)
        else:
            print(f"MISS {decoded_src}")
            missing.append(decoded_src)

    print(f"\n완료: {len(copied)}건 복사, {len(missing)}건 누락")
    if missing:
        print("누락 목록:")
        for m in missing:
            print(f"  - {m}")
        print("\n[참고] 실제 존재하는 파일명:")
        for d in sorted(decoded_map.keys()):
            print(f"  {d}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--zipdir', required=True, help='압축 해제된 zip 폴더 경로')
    parser.add_argument('--mapping', required=True, help='image_mapping.json 경로')
    parser.add_argument('--images-dir', default='images', help='출력 images 폴더 (기본: images/)')
    parser.add_argument('--dry-run', action='store_true', help='복사하지 않고 결과만 출력')
    args = parser.parse_args()

    run(args.zipdir, args.mapping, args.images_dir, args.dry_run)
