class Trmd < Formula
  include Language::Python::Virtualenv

  desc "Translate Markdown using OpenAI"
  homepage "https://github.com/rioriost/homebrew-trmd/"
  url "https://files.pythonhosted.org/packages/1c/b8/30d171b0b65442cb6044f8463322abfd09595b63baa06ef48e33d591c967/trmd-0.1.5.tar.gz"
  sha256 "c4d5b6b54dcf9b7d4fe488d43cfa997ae0e06fdd9f95e969a1471cd2bacb1048"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai"
  end

  test do
    system "#{bin}/trmd", "--help"
  end
end
