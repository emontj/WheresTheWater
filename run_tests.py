import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), 'production'))

if __name__ == "__main__":
    pytest.main(['tests', '--maxfail=5', '--disable-warnings'])
