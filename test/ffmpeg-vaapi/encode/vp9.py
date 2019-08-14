###
### Copyright (C) 2018-2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ..util import *
from .encoder import EncoderTest

spec = load_test_spec("vp9", "encode", "8bit")

class VP9EncoderTest(EncoderTest):
  def before(self):
    vars(self).update(
      codec   = "vp9",
      ffenc   = "vp9_vaapi",
      profile = "profile0",
    )
    super(VP9EncoderTest, self).before()

  def get_file_ext(self):
    return "ivf"

  def get_vaapi_profile(self):
    return "VAProfileVP9Profile0"

class cqp(VP9EncoderTest):
  @slash.requires(*platform.have_caps("encode", "vp9_8"))
  @slash.requires(*have_ffmpeg_encoder("vp9_vaapi"))
  @slash.parametrize(*gen_vp9_cqp_parameters(spec))
  def test(self, case, ipmode, qp, quality, refmode, looplvl, loopshp):
    slash.logger.notice("NOTICE: 'quality' parameter unused (not supported by plugin)")
    slash.logger.notice("NOTICE: 'refmode' parameter unused (not supported by plugin)")
    self.caps = platform.get_caps("encode", "vp9_8")
    vars(self).update(spec[case].copy())
    vars(self).update(
      case      = case,
      gop       = 30 if ipmode != 0 else 1,
      looplvl   = looplvl,
      loopshp   = loopshp,
      qp        = qp,
      rcmode    = "cqp",
    )
    self.encode()

class cbr(VP9EncoderTest):
  @slash.requires(*platform.have_caps("encode", "vp9_8"))
  @slash.requires(*have_ffmpeg_encoder("vp9_vaapi"))
  @slash.parametrize(*gen_vp9_cbr_parameters(spec))
  def test(self, case, gop, bitrate, fps, refmode, looplvl, loopshp):
    slash.logger.notice("NOTICE: 'refmode' parameter unused (not supported by plugin)")
    self.caps = platform.get_caps("encode", "vp9_8")
    vars(self).update(spec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      frames    = vars(self).get("brframes", self.frames),
      gop       = gop,
      looplvl   = looplvl,
      loopshp   = loopshp,
      maxrate   = bitrate,
      minrate   = bitrate,
      rcmode    = "cbr",
    )
    self.encode()

class vbr(VP9EncoderTest):
  @slash.requires(*platform.have_caps("encode", "vp9_8"))
  @slash.requires(*have_ffmpeg_encoder("vp9_vaapi"))
  @slash.parametrize(*gen_vp9_vbr_parameters(spec))
  def test(self, case, gop, bitrate, fps, refmode, quality, looplvl, loopshp):
    slash.logger.notice("NOTICE: 'quality' parameter unused (not supported by plugin)")
    slash.logger.notice("NOTICE: 'refmode' parameter unused (not supported by plugin)")
    self.caps = platform.get_caps("encode", "vp9_8")
    vars(self).update(spec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      frames    = vars(self).get("brframes", self.frames),
      gop       = gop,
      looplvl   = looplvl,
      loopshp   = loopshp,
      maxrate   = bitrate * 2, # target percentage 50%
      minrate   = bitrate,
      rcmode    = "vbr",
    )
    self.encode()
