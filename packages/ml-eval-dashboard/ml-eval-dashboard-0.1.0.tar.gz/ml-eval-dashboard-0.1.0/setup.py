from setuptools import setup, find_packages

setup(
    name='ml-eval-dashboard',
    version='0.1.0',
    description='Reusable ML Evaluation Dashboard built with Streamlit',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'ml-eval-dashboard=ml_eval_dashboard.dashboard:run_dashboard'
        ],
    },
)
