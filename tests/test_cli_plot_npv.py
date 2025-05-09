import unittest
import subprocess
import os

class TestCliPlotNpv(unittest.TestCase):
    def test_compare_cli_plot_generation(self):
        output_file = "docs/tmp_compare_test.png"
        cmd = [
            "python", "-m", "finance_core.plot_npv", "-1000", "500", "400", 
            "--compare", "-1000", "500", "600", 
            "--return_irr", 
            "--save_path", output_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Ensure command runs successfully
        assert result.returncode == 0, f"CLI failed with stderr: {result.stderr}"
        # Ensure image file was saved
        assert os.path.exists(output_file), f"Plot file was not created"
        # Ensure IRR was printed
        assert "IRR" in result.stdout, "IRR output missing"

        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    unittest.main()