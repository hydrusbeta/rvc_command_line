import argparse
import soundfile
import sys
from infer.modules.vc.modules import VC
from configs.config import Config

# todo: Add options for batch processing

parser = argparse.ArgumentParser(prog='Retrieval-Based Voice Conversion',
                                 description='A Voice Conversion framework based on VITS')
parser.add_argument('-v', '--voice',           type=str,                       required=True)
parser.add_argument('--sid',                   type=int,   default=0)
parser.add_argument('-i', '--input_filepath',  type=str,                       required=True)
parser.add_argument('--transpose',             type=int,   default=0)
parser.add_argument('--f0_filepath',           type=str,   default=None)
parser.add_argument('--f0_method',             type=str,   default='harvest')
parser.add_argument('--index_filepath',        type=str,   default='')
parser.add_argument('--index_ratio',           type=float, default=1)
parser.add_argument('--filter_radius',         type=int,   default=3)
parser.add_argument('--resample_rate',         type=int,   default=0)
parser.add_argument('--rms_mix_ratio',         type=float, default=1)
parser.add_argument('--protect',               type=float, default=0.33)
parser.add_argument('-o', '--output_filepath', type=str,                       required=True)
args = parser.parse_args()

# infer-web.py parses sys.argv arguments upon import. Erase all existing arguments to prevent an "unrecognized
# argument" error and insert the "commandlinemode" argument which will prevent the server from automatically starting.
sys.argv = ['', '--commandlinemode']

# Load the model
config = Config()
# todo override config.device with "cpu" or "cuda:#". Alternatively, use RVC's built-in CLI.
vc = VC(config)
_ = vc.get_vc(args.voice, None, None)

# Perform inference
_, (output_samplerate, audio_output) = vc.vc_single(args.sid,
                                                    args.input_filepath,
                                                    args.transpose,
                                                    args.f0_filepath,
                                                    args.f0_method,
                                                    args.index_filepath,
                                                    '',
                                                    args.index_ratio,
                                                    args.filter_radius,
                                                    args.resample_rate,
                                                    args.rms_mix_ratio,
                                                    args.protect)

# Write the output file
soundfile.write(args.output_filepath, audio_output, output_samplerate, format='FLAC')
