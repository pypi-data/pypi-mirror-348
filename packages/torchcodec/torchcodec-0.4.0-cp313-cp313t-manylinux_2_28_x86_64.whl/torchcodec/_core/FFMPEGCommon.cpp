// Copyright (c) Meta Platforms, Inc. and affiliates.
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

#include "src/torchcodec/_core/FFMPEGCommon.h"

#include <c10/util/Exception.h>

namespace facebook::torchcodec {

AutoAVPacket::AutoAVPacket() : avPacket_(av_packet_alloc()) {
  TORCH_CHECK(avPacket_ != nullptr, "Couldn't allocate avPacket.");
}

AutoAVPacket::~AutoAVPacket() {
  av_packet_free(&avPacket_);
}

ReferenceAVPacket::ReferenceAVPacket(AutoAVPacket& shared)
    : avPacket_(shared.avPacket_) {}

ReferenceAVPacket::~ReferenceAVPacket() {
  av_packet_unref(avPacket_);
}

AVPacket* ReferenceAVPacket::get() {
  return avPacket_;
}

AVPacket* ReferenceAVPacket::operator->() {
  return avPacket_;
}

AVCodecOnlyUseForCallingAVFindBestStream
makeAVCodecOnlyUseForCallingAVFindBestStream(const AVCodec* codec) {
#if LIBAVCODEC_VERSION_INT < AV_VERSION_INT(59, 18, 100)
  return const_cast<AVCodec*>(codec);
#else
  return codec;
#endif
}

std::string getFFMPEGErrorStringFromErrorCode(int errorCode) {
  char errorBuffer[AV_ERROR_MAX_STRING_SIZE] = {0};
  av_strerror(errorCode, errorBuffer, AV_ERROR_MAX_STRING_SIZE);
  return std::string(errorBuffer);
}

int64_t getDuration(const UniqueAVFrame& avFrame) {
#if LIBAVUTIL_VERSION_MAJOR < 58
  return avFrame->pkt_duration;
#else
  return avFrame->duration;
#endif
}

int getNumChannels(const UniqueAVFrame& avFrame) {
#if LIBAVFILTER_VERSION_MAJOR > 8 || \
    (LIBAVFILTER_VERSION_MAJOR == 8 && LIBAVFILTER_VERSION_MINOR >= 44)
  return avFrame->ch_layout.nb_channels;
#else
  return av_get_channel_layout_nb_channels(avFrame->channel_layout);
#endif
}

int getNumChannels(const UniqueAVCodecContext& avCodecContext) {
#if LIBAVFILTER_VERSION_MAJOR > 8 || \
    (LIBAVFILTER_VERSION_MAJOR == 8 && LIBAVFILTER_VERSION_MINOR >= 44)
  return avCodecContext->ch_layout.nb_channels;
#else
  return avCodecContext->channels;
#endif
}

void setDefaultChannelLayout(
    UniqueAVCodecContext& avCodecContext,
    int numChannels) {
#if LIBAVFILTER_VERSION_MAJOR > 7 // FFmpeg > 4
  AVChannelLayout channel_layout;
  av_channel_layout_default(&channel_layout, numChannels);
  avCodecContext->ch_layout = channel_layout;
#else
  uint64_t channel_layout = av_get_default_channel_layout(numChannels);
  avCodecContext->channel_layout = channel_layout;
  avCodecContext->channels = numChannels;
#endif
}

void setChannelLayout(
    UniqueAVFrame& dstAVFrame,
    const UniqueAVCodecContext& avCodecContext) {
#if LIBAVFILTER_VERSION_MAJOR > 7 // FFmpeg > 4
  auto status = av_channel_layout_copy(
      &dstAVFrame->ch_layout, &avCodecContext->ch_layout);
  TORCH_CHECK(
      status == AVSUCCESS,
      "Couldn't copy channel layout to avFrame: ",
      getFFMPEGErrorStringFromErrorCode(status));
#else
  dstAVFrame->channel_layout = avCodecContext->channel_layout;
  dstAVFrame->channels = avCodecContext->channels;

#endif
}

namespace {
#if LIBAVFILTER_VERSION_MAJOR > 7 // FFmpeg > 4

// Returns:
// - the srcAVFrame's channel layout if srcAVFrame has desiredNumChannels
// - the default channel layout with desiredNumChannels otherwise.
AVChannelLayout getDesiredChannelLayout(
    int desiredNumChannels,
    const UniqueAVFrame& srcAVFrame) {
  AVChannelLayout desiredLayout;
  if (desiredNumChannels == getNumChannels(srcAVFrame)) {
    desiredLayout = srcAVFrame->ch_layout;
  } else {
    av_channel_layout_default(&desiredLayout, desiredNumChannels);
  }
  return desiredLayout;
}

#else

// Same as above
int64_t getDesiredChannelLayout(
    int desiredNumChannels,
    const UniqueAVFrame& srcAVFrame) {
  int64_t desiredLayout;
  if (desiredNumChannels == getNumChannels(srcAVFrame)) {
    desiredLayout = srcAVFrame->channel_layout;
  } else {
    desiredLayout = av_get_default_channel_layout(desiredNumChannels);
  }
  return desiredLayout;
}
#endif
} // namespace

// Sets dstAVFrame' channel layout to getDesiredChannelLayout(): see doc above
void setChannelLayout(
    UniqueAVFrame& dstAVFrame,
    const UniqueAVFrame& srcAVFrame,
    int desiredNumChannels) {
#if LIBAVFILTER_VERSION_MAJOR > 7 // FFmpeg > 4
  AVChannelLayout desiredLayout =
      getDesiredChannelLayout(desiredNumChannels, srcAVFrame);
  auto status = av_channel_layout_copy(&dstAVFrame->ch_layout, &desiredLayout);
  TORCH_CHECK(
      status == AVSUCCESS,
      "Couldn't copy channel layout to avFrame: ",
      getFFMPEGErrorStringFromErrorCode(status));
#else
  dstAVFrame->channel_layout =
      getDesiredChannelLayout(desiredNumChannels, srcAVFrame);
  dstAVFrame->channels = desiredNumChannels;
#endif
}

SwrContext* createSwrContext(
    AVSampleFormat srcSampleFormat,
    AVSampleFormat desiredSampleFormat,
    int srcSampleRate,
    int desiredSampleRate,
    const UniqueAVFrame& srcAVFrame,
    int desiredNumChannels) {
  SwrContext* swrContext = nullptr;
  int status = AVSUCCESS;
#if LIBAVFILTER_VERSION_MAJOR > 7 // FFmpeg > 4
  AVChannelLayout desiredLayout =
      getDesiredChannelLayout(desiredNumChannels, srcAVFrame);
  status = swr_alloc_set_opts2(
      &swrContext,
      &desiredLayout,
      desiredSampleFormat,
      desiredSampleRate,
      &srcAVFrame->ch_layout,
      srcSampleFormat,
      srcSampleRate,
      0,
      nullptr);

  TORCH_CHECK(
      status == AVSUCCESS,
      "Couldn't create SwrContext: ",
      getFFMPEGErrorStringFromErrorCode(status));
#else
  int64_t desiredLayout =
      getDesiredChannelLayout(desiredNumChannels, srcAVFrame);
  swrContext = swr_alloc_set_opts(
      nullptr,
      desiredLayout,
      desiredSampleFormat,
      desiredSampleRate,
      srcAVFrame->channel_layout,
      srcSampleFormat,
      srcSampleRate,
      0,
      nullptr);
#endif

  TORCH_CHECK(swrContext != nullptr, "Couldn't create swrContext");
  status = swr_init(swrContext);
  TORCH_CHECK(
      status == AVSUCCESS,
      "Couldn't initialize SwrContext: ",
      getFFMPEGErrorStringFromErrorCode(status),
      ". If the error says 'Invalid argument', it's likely that you are using "
      "a buggy FFmpeg version. FFmpeg4 is known to fail here in some "
      "valid scenarios. Try to upgrade FFmpeg?");
  return swrContext;
}

UniqueAVFrame convertAudioAVFrameSamples(
    const UniqueSwrContext& swrContext,
    const UniqueAVFrame& srcAVFrame,
    AVSampleFormat desiredSampleFormat,
    int desiredSampleRate,
    int desiredNumChannels) {
  UniqueAVFrame convertedAVFrame(av_frame_alloc());
  TORCH_CHECK(
      convertedAVFrame,
      "Could not allocate frame for sample format conversion.");

  convertedAVFrame->format = static_cast<int>(desiredSampleFormat);

  convertedAVFrame->sample_rate = desiredSampleRate;
  int srcSampleRate = srcAVFrame->sample_rate;
  if (srcSampleRate != desiredSampleRate) {
    // Note that this is an upper bound on the number of output samples.
    // `swr_convert()` will likely not fill convertedAVFrame with that many
    // samples if sample rate conversion is needed. It will buffer the last few
    // ones because those require future samples. That's also why we reset
    // nb_samples after the call to `swr_convert()`.
    // We could also use `swr_get_out_samples()` to determine the number of
    // output samples, but empirically `av_rescale_rnd()` seems to provide a
    // tighter bound.
    convertedAVFrame->nb_samples = av_rescale_rnd(
        swr_get_delay(swrContext.get(), srcSampleRate) + srcAVFrame->nb_samples,
        desiredSampleRate,
        srcSampleRate,
        AV_ROUND_UP);
  } else {
    convertedAVFrame->nb_samples = srcAVFrame->nb_samples;
  }

  setChannelLayout(convertedAVFrame, srcAVFrame, desiredNumChannels);

  auto status = av_frame_get_buffer(convertedAVFrame.get(), 0);
  TORCH_CHECK(
      status == AVSUCCESS,
      "Could not allocate frame buffers for sample format conversion: ",
      getFFMPEGErrorStringFromErrorCode(status));

  auto numConvertedSamples = swr_convert(
      swrContext.get(),
      convertedAVFrame->data,
      convertedAVFrame->nb_samples,
      static_cast<const uint8_t**>(
          const_cast<const uint8_t**>(srcAVFrame->data)),
      srcAVFrame->nb_samples);
  // numConvertedSamples can be 0 if we're downsampling by a great factor and
  // the first frame doesn't contain a lot of samples. It should be handled
  // properly by the caller.
  TORCH_CHECK(
      numConvertedSamples >= 0,
      "Error in swr_convert: ",
      getFFMPEGErrorStringFromErrorCode(numConvertedSamples));

  // See comment above about nb_samples
  convertedAVFrame->nb_samples = numConvertedSamples;

  return convertedAVFrame;
}

void setFFmpegLogLevel() {
  auto logLevel = AV_LOG_QUIET;
  const char* logLevelEnvPtr = std::getenv("TORCHCODEC_FFMPEG_LOG_LEVEL");
  if (logLevelEnvPtr != nullptr) {
    std::string logLevelEnv(logLevelEnvPtr);
    if (logLevelEnv == "QUIET") {
      logLevel = AV_LOG_QUIET;
    } else if (logLevelEnv == "PANIC") {
      logLevel = AV_LOG_PANIC;
    } else if (logLevelEnv == "FATAL") {
      logLevel = AV_LOG_FATAL;
    } else if (logLevelEnv == "ERROR") {
      logLevel = AV_LOG_ERROR;
    } else if (logLevelEnv == "WARNING") {
      logLevel = AV_LOG_WARNING;
    } else if (logLevelEnv == "INFO") {
      logLevel = AV_LOG_INFO;
    } else if (logLevelEnv == "VERBOSE") {
      logLevel = AV_LOG_VERBOSE;
    } else if (logLevelEnv == "DEBUG") {
      logLevel = AV_LOG_DEBUG;
    } else if (logLevelEnv == "TRACE") {
      logLevel = AV_LOG_TRACE;
    } else {
      TORCH_CHECK(
          false,
          "Invalid TORCHCODEC_FFMPEG_LOG_LEVEL: ",
          logLevelEnv,
          ". Use e.g. 'QUIET', 'PANIC', 'VERBOSE', etc.");
    }
  }
  av_log_set_level(logLevel);
}

AVIOContext* avioAllocContext(
    uint8_t* buffer,
    int buffer_size,
    int write_flag,
    void* opaque,
    AVIOReadFunction read_packet,
    AVIOWriteFunction write_packet,
    AVIOSeekFunction seek) {
  return avio_alloc_context(
      buffer,
      buffer_size,
      write_flag,
      opaque,
      read_packet,
// The buf parameter of the write function is not const before FFmpeg 7.
#if LIBAVFILTER_VERSION_MAJOR >= 10 // FFmpeg >= 7
      write_packet,
#else
      reinterpret_cast<AVIOWriteFunctionOld>(write_packet),
#endif
      seek);
}

} // namespace facebook::torchcodec
