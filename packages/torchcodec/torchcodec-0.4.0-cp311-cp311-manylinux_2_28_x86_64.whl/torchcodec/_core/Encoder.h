#pragma once
#include <torch/types.h>
#include "src/torchcodec/_core/AVIOBytesContext.h"
#include "src/torchcodec/_core/FFMPEGCommon.h"

namespace facebook::torchcodec {
class AudioEncoder {
 public:
  ~AudioEncoder();

  // TODO-ENCODING: document in public docs that bit_rate value is only
  // best-effort, matching to the closest supported bit_rate. I.e. passing 1 is
  // like passing 0, which results in choosing the minimum supported bit rate.
  // Passing 44_100 could result in output being 44000 if only 44000 is
  // supported.
  AudioEncoder(
      const torch::Tensor wf,
      // The *output* sample rate. We can't really decide for the user what it
      // should be. Particularly, the sample rate of the input waveform should
      // match this, and that's up to the user. If sample rates don't match,
      // encoding will still work but audio will be distorted.
      int sampleRate,
      std::string_view fileName,
      std::optional<int64_t> bitRate = std::nullopt);
  AudioEncoder(
      const torch::Tensor wf,
      int sampleRate,
      std::string_view formatName,
      std::unique_ptr<AVIOToTensorContext> avioContextHolder,
      std::optional<int64_t> bitRate = std::nullopt);
  void encode();
  torch::Tensor encodeToTensor();

 private:
  void initializeEncoder(
      int sampleRate,
      std::optional<int64_t> bitRate = std::nullopt);
  void encodeInnerLoop(
      AutoAVPacket& autoAVPacket,
      const UniqueAVFrame& srcAVFrame);
  void flushBuffers();

  UniqueEncodingAVFormatContext avFormatContext_;
  UniqueAVCodecContext avCodecContext_;
  int streamIndex_;
  UniqueSwrContext swrContext_;

  const torch::Tensor wf_;

  // Stores the AVIOContext for the output tensor buffer.
  std::unique_ptr<AVIOToTensorContext> avioContextHolder_;

  bool encodeWasCalled_ = false;
};
} // namespace facebook::torchcodec
