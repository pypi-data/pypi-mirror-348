import os
import urllib.request
from gensim.models import KeyedVectors
import gzip
import shutil
from pathlib import Path


class Embedder:
    available_models = {
        "fasttext-d300-w5-cbow-naab": "https://amirivojdan.io/shekar-data/fasttext_d300_w5_cbow_naab.vec.gz",
        "fasttext-d100-w10-cbow-blogs": "https://amirivojdan.io/shekar-data/fasttext_d100_w10_cbow_blogs.vec.gz",
    }

    def __init__(self, model_name: str = "fasttext-d100-w10-cbow-blogs"):
        """
        Initialize the Embedding instance.
        Args:
            model (str, optional): The name of the model to load. Defaults to "fasttext-300-naab".
        """

        self.model = self.load_model(model_name)

    def __getitem__(self, word: str):
        """
        Get the vector representation of the specified word.
        Args:
            word (str): The word to get its vector representation.
        Returns:
            numpy.ndarray: The vector representation of the specified word.
        """
        try:
            return self.model[word]
        except KeyError:
            return None

    def most_similar(self, word: str, topn: int = 10):
        """
        Get the top N most similar words to the specified word.
        Args:
            word (str): The word to find its most similar words.
            topn (int, optional): The number of most similar words to return. Defaults to 10.
        Returns:
            list: The list of the top N most similar words to the specified word.
        """

        try:
            return self.model.most_similar(word, topn=topn)
        except KeyError:
            return None

    def load_model(self, model_name: str):
        """
        Load the specified model.
        Args:
            model (str): The name of the model to load.
        Returns:
            gensim.models.KeyedVectors: The loaded model.
        """
        model_url = self.available_models[model_name]
        model_file_name = model_name.replace("-", "_") + ".vec.gz"
        cache_dir = Path.home() / ".shekar"
        model_zip_path = cache_dir / model_file_name
        model_path = model_zip_path.with_suffix("")  # Remove .gz

        cache_dir.mkdir(parents=True, exist_ok=True)

        if not model_path.exists():
            if not model_zip_path.exists():
                self.download_model(model_url, model_zip_path)

            with gzip.open(model_zip_path, "rb") as f_in:
                with open(model_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

        if os.path.exists(model_zip_path):
            os.remove(model_zip_path)

        try:
            return KeyedVectors.load_word2vec_format(model_path, binary=True)
        except Exception:
            return None

    @staticmethod
    def download_model(url: str, dest_path: Path):
        """
        Download the model from the specified URL to the destination path.
        Args:
            url (str): The URL of the model to download.
            dest_path (Path): The destination path to save the downloaded model.
        """
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as response:
                total_length = response.getheader("content-length")
                if total_length is None:  # no content length header
                    with open(dest_path, "wb") as out_file:
                        out_file.write(response.read())
                else:
                    total_length = int(total_length)
                    with open(dest_path, "wb") as out_file:
                        downloaded = 0
                        while True:
                            data = response.read(1024)
                            if not data:
                                break
                            downloaded += len(data)
                            out_file.write(data)
                            done = int(50 * downloaded / total_length)
                            print(
                                f"\r[{'=' * done}{' ' * (50 - done)}] {done * 2}%",
                                end="",
                            )
                    return True
        except Exception as e:
            print(f"Error downloading the model: {e}")
            return False


if __name__ == "__main__":
    emb = Embedder()
    print(emb.model.doesnt_match("گل درخت ماشین سنگ".split()))
