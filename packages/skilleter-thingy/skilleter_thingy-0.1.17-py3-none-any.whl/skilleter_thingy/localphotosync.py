#!/usr/bin/env python3

"""
Sync a directory tree full of photos into a tree organised by year, month and date
"""

import os
import sys
import datetime
import logging
import argparse
import glob
import re
import shutil
import PIL
import imagehash

from collections import defaultdict
from enum import Enum

from PIL import Image, ExifTags

import thingy.colour as colour

################################################################################

# Default locations for local storage of photos and videos

DEFAULT_PHOTO_DIR = os.path.expanduser('~/Pictures')
DEFAULT_VIDEO_DIR = os.path.expanduser('~/Videos')

# File extensions (case-insensitive)

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', )
VIDEO_EXTENSIONS = ('.mp4', '.mov', )
IGNORE_EXTENSIONS = ('.ini', )

# Enum of filetypes

class FileType(Enum):
    IMAGE = 0
    VIDEO = 1
    UNKNOWN = 2
    IGNORE = 3

# Regexes for matching date strings

YYYY_MM_DD_re = re.compile(r'^(\d{4}):(\d{2}):(\d{2})')
IMG_DATE_re = re.compile(r'(?:IMG|VID)[-_](\d{4})(\d{2})(\d{2})[-_.].*')

GENERAL_DATE_re = re.compile(r'(\d{4})[-_ ](\d{2})[-_ ](\d{2})')

YEAR_MONTH_PATH_re = re.compile(r'/(\d{4})/(\d{2})/')

YYYY_MM_re = re.compile(r'(\d{4})-(\d{2})')

DUP_RE = re.compile(r'(.*) \{aalq_f.*\}(.*)')

# Date format for YYYY-MM

DATE_FORMAT = '%Y-%m'

# If two pictures with the same name prefix have a hash differing by less than
# this then we don't hash the duplicates

MIN_HASH_DIFF = 15

################################################################################

def parse_yyyymm(datestr):
    """Convert a date string in the form YYYY-MM to a datetime.date"""

    date_match = YYYY_MM_re.fullmatch(datestr)

    if not date_match:
        colour.error(f'ERROR: Invalid date: {datestr}')

    return datetime.date(int(date_match.group(1)), int(date_match.group(2)), day=1)

################################################################################

def parse_command_line():
    """Parse and validate the command line options"""

    parser = argparse.ArgumentParser(description='Sync photos from Google Photos')

    today = datetime.date.today()

    parser.add_argument('--verbose', '-v', action='store_true', help='Output verbose status information')
    parser.add_argument('--dryrun', '--dry-run', '-D', action='store_true', help='Just list files to be copied, without actually copying them')
    parser.add_argument('--picturedir', '-P', action='store', default=DEFAULT_PHOTO_DIR, help=f'Location of local picture storage directory (defaults to {DEFAULT_PHOTO_DIR})')
    parser.add_argument('--videodir', '-V', action='store', default=DEFAULT_VIDEO_DIR, help=f'Location of local video storage directory (defaults to {DEFAULT_VIDEO_DIR})')
    parser.add_argument('--skip-no-day', '-z', action='store_true', help='Don\'t sync files where the day of the month could not be determined')
    parser.add_argument('--path', '-p', action='store', default=None, help='Path to sync from')
    parser.add_argument('action', nargs='*', help='Actions to perform (report or sync)')

    args = parser.parse_args()

    if not args.path:
        colour.error('You must specify a source directory')

    # Configure debugging

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    # Report parameters if verbose

    logging.debug('Source:    %s', args.path)
    logging.debug('Pictures:  %s', args.picturedir)
    logging.debug('Videos:    %s', args.videodir)
    logging.debug('Dry run:   %d', args.dryrun)

    args.local_dir = {'photo': args.picturedir, 'video': args.videodir}

    return args

################################################################################

def get_exif_data(image):
    """Return EXIF data for the image as a dictionary"""

    try:
        img = Image.open(image)

        img_exif = img.getexif()
    except OSError as exc:
        logging.info('Error reading EXIF data for %s - %s', image, exc)
        img_exif = None

    result = {}

    if img_exif is None:
        return result

    for key, val in img_exif.items():
        if key in ExifTags.TAGS:
            result[ExifTags.TAGS[key]] = val
        else:
            result[key] = val

    return result

################################################################################

def get_filetype(filename):
    """Return the type of a file"""

    _, ext = os.path.splitext(filename)

    ext = ext.lower()

    if ext in IMAGE_EXTENSIONS:
        return FileType.IMAGE

    if ext in VIDEO_EXTENSIONS:
        return FileType.VIDEO

    if ext in IGNORE_EXTENSIONS:
        return FileType.IGNORE

    return FileType.UNKNOWN

################################################################################

def find_files(directory_wildcards):
    """Return a list of all the files in the specified directory tree, which can contain wildcards,
       as 3 lists; pictures, videos and unknown."""

    image_list = {}
    video_list = {}
    unknown_list = []

    logging.info('Reading files in the directory tree(s) at %s', ', '.join(directory_wildcards))

    for directory_wildcard in directory_wildcards:
        directories = glob.glob(directory_wildcard)

        for directory in directories:
            for root, _, files in os.walk(directory):
                logging.debug('Reading %s', root)

                for file in files:
                    filepath = os.path.join(root, file)

                    file_type = get_filetype(filepath)

                    if file_type == FileType.IMAGE:
                        try:
                            exif = get_exif_data(filepath)

                            image_list[filepath] = exif
                        except PIL.UnidentifiedImageError:
                            colour.write(f'[BOLD:WARNING:] Unable to get EXIF data from [BLUE:{filepath}]')
                            image_list[filepath] = {}

                    elif file_type == FileType.VIDEO:
                        # TODO: Is there a way of getting EXIF-type data from video files? (https://thepythoncode.com/article/extract-media-metadata-in-python but does it include date info?)
                        video_list[filepath] = {}

                    elif file_type == FileType.UNKNOWN:
                        unknown_list.append(filepath)

    logging.info('Read %s image files', len(image_list))
    logging.info('Read %s video files', len(video_list))
    logging.info('Read %s unknown files', len(unknown_list))

    return image_list, video_list, unknown_list

################################################################################

def get_media_date(name, info):
    """Try and determine the date for a given picture. Returns y, m, d or
       None, None, None"""

    # If the EXIF data has the date & time, just return that

    if 'DateTimeOriginal' in info:
        original_date_time = info['DateTimeOriginal']

        date_match = YYYY_MM_DD_re.match(original_date_time)
        if date_match:
            year = date_match.group(1)
            month = date_match.group(2)
            day = date_match.group(3)

            return year, month, day

    # No EXIF date and time, try and parse it out of the filename

    picture_name = os.path.basename(name)

    date_match = IMG_DATE_re.match(picture_name) or GENERAL_DATE_re.search(picture_name)

    if date_match:
        year = date_match.group(1)
        month = date_match.group(2)
        day = date_match.group(3)

        return year, month, day

    date_match = YEAR_MONTH_PATH_re.search(name)
    if date_match:
        year = date_match.group(1)
        month = date_match.group(2)
        day = '00'

        return year, month, day

    # A miserable failure

    return None, None, None

################################################################################

def sync_media_local(dryrun, skip_no_day, media_files, destination_dir):
    """Sync files from the cache to local storage"""

    # Iterate through the list of remote media_files to try work out the date and
    # time so that we can copy it the correct local location

    for media_file in media_files:
        year, month, day = get_media_date(media_file, media_files[media_file])

        # If specified, skip files where the day of the month could not be determined

        if skip_no_day and day == '00':
            day = None

        if year and month and day:
            destination_media_file_path = os.path.join(destination_dir, year, f'{year}-{month}-{day}', os.path.basename(media_file))

            if os.path.exists(destination_media_file_path):
                colour.write(f'[RED:WARNING]: Destination [BLUE:{destination_media_file_path}] already exists - file will not be overwritten!')
            else:
                destination_dir_name = os.path.dirname(destination_media_file_path)

                colour.write(f'Copying [BLUE:{media_file}] to [BLUE:{destination_dir_name}]')

                if not dryrun:
                    os.makedirs(destination_dir_name, exist_ok=True)

                    shutil.copyfile(media_file, destination_media_file_path)
        else:
            colour.write(f'[RED:ERROR]: Unable to determine where to copy [BLUE:{media_file}]')

################################################################################

def local_directory(args, mediatype, year, month):
    """Return the location of the local picture directory for the specified year/month"""

    return os.path.join(args.local_dir[mediatype], str(year), f'{year}-{month:02}')

################################################################################

def media_sync(dryrun, skip_no_day, media, media_files, local_dir):
    """Given a media type and list of local and remote files of the type, check
       for out-of-sync files and sync any missing remote files to local storage"""

    # Get the list of local and remote names of the specified media type
    # TODO: Could be a problem if we have multiple files with the same name (e.g. in different months)

    names = {'local': {}, 'remote': {}}

    for name in media_files['local']:
        names['local'][os.path.basename(name)] = name

    for name in media_files['remote']:
        names['remote'][os.path.basename(name)] = name

    # Find matches and remove them

    matching = 0
    for name in names['local']:
        if name in names['remote']:
            matching += 1

            del media_files['remote'][names['remote'][name]]
            del media_files['local'][names['local'][name]]

    if matching:
        colour.write(f'    [BOLD:{matching} {media} files are in sync]')
    else:
        colour.write(f'    [BOLD:No {media} files are in sync]')

    if media_files['local']:
        colour.write(f'    [BOLD:{len(media_files["local"])} local {media} files are out of sync]')
    else:
        colour.write(f'    [BOLD:No local {media} files are out of sync]')

    if media_files['remote']:
        colour.write(f'    [BOLD:{len(media_files["remote"])} remote {media} files are out of sync]')
        sync_media_local(dryrun, skip_no_day, media_files['remote'], local_dir)
    else:
        colour.write(f'    [BOLD:No remote {media} files are out of sync]')

    colour.write('')

################################################################################

# TODO: Tidy this up!
def remove_duplicates(media_files):
    """Look for remote files which have an original and multiple
       copies and remove the copies from the list of files to consider using the
       imagehash library to detect duplicate or near-duplicate files.
    """

    print('Checking for duplicate files')

    # Originals can have upper or lower case extensions, copies only tend to have lower
    # case, so build a lower case to original lookup table

    names = {name.lower():name for name in media_files}

    duplicates = defaultdict(list)

    # Build a list of duplicates for each filename in the list - i.e. files with the same
    # prefix and a suffix matching DUP_RE, indexed by the base filename (without the suffix)

    for entry in names:
        orig_match = DUP_RE.fullmatch(entry)
        if orig_match:
            original = orig_match.group(1) + orig_match.group(2)

            duplicates[original].append(entry)

    # Now use the imagehash library to check each list of maybe-duplicate files
    # to build a list of actual duplicates (or at least nearly-indistinguishable images)
    # TODO: Better to build list of all hashes, then find near-duplicates

    actual_duplicates = set()
    for entry, dupes in duplicates.items():
        # If the base file (no suffix) exists use that as the base, otherwise
        # use the first duplicate (we can have a situation where we have duplicates
        # and no original).

        hash_list = defaultdict(list)

        # Start with the base file, it it exists

        if entry in names:
            try:
                base_hash = str(imagehash.average_hash(Image.open(names[entry])))

                hash_list[base_hash].append(names[entry])
            except OSError:
                pass

        # Calculate the hash of each of the potential duplicates and if they
        # are close enough to the base hash, then add them to the real duplicate list

        for entry in dupes:
            filename = names[entry]
            try:
                dupe_hash = str(imagehash.average_hash(Image.open(filename)))

                hash_list[dupe_hash].append(filename)
            except OSError:
                colour.write(f'[BOLD:WARNING]: Unable to read {filename}')

        # Remove entries with identical hash values

        for dupes in hash_list:
            for dupe in hash_list[dupes][1:]:
                actual_duplicates.add(dupe)
            hash_list[dupes] = hash_list[dupes][0]

        # Look for adjaced entries in the sorted list of hash values that differ by less then the minimum
        # and remove the duplicates

        hash_values = sorted(hash_list.keys())
        logging.debug('Hash values for duplicates: %s', hash_values)

        for i in range(len(hash_values)-1):
            if int(hash_values[i+1], 16) - int(hash_values[i], 16) < MIN_HASH_DIFF:
                actual_duplicates.add(hash_list[hash_values[i+1]])

    # Remove all the entries in the real duplicates list

    for entry in actual_duplicates:
        logging.info('Removing %s as a (near-)duplicate', os.path.basename(entry))
        del media_files[entry]

################################################################################

def photo_sync(args):
    """Synchronise the photos"""

    colour.write('[GREEN:%s]' % '-'*80)

    # Read the pictures and their EXIF data to get the dates

    media_files = {'photo': {}, 'video': {}}
    unknown_files = {}

    media_files['photo']['remote'], media_files['video']['remote'], unknown_files['remote'] = find_files([args.path])
    media_files['photo']['local'], media_files['video']['local'], unknown_files['local'] = find_files([args.picturedir, args.videodir])

    for media in ('photo', 'video'):
        remove_duplicates(media_files[media]['remote'])

    colour.write('[GREEN:%s]' % '-'*80)

    media_sync(args.dryrun, args.skip_no_day, media, media_files['photo'], args.picturedir)
    media_sync(args.dryrun, args.skip_no_day, media, media_files['video'], args.videodir)

################################################################################

def main():
    """Entry point"""

    # Handle the command line

    args = parse_command_line()

    photo_sync(args)

################################################################################

def localphotosync():
    """Entry point"""
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(2)

################################################################################

if __name__ == '__main__':
    localphotosync()
