from dataclasses import dataclass


@dataclass
class ModelConfig:
    # visdom and HTML visualization parameters
    display_freq: int = 400
    display_ncols: int = 4
    display_id: int = 1
    display_server: str = "http://localhost"
    display_env: str = 'main'
    display_port: int = 8097
    update_html_freq: int = 1000
    print_freq: int = 100
    no_html: bool = False

    # network saving and loading parameters
    save_latest_freq: int = 5000
    save_epoch_freq: int = 100
    save_by_iter: bool = False
    continue_train: bool = False
    epoch_count: int = 1
    phase: str = 'train'

    # training parameters
    n_epochs: int = 100
    n_epochs_decay: int = 100
    beta1: float = 0.5
    lr: float = 0.0002
    gan_mode: str = 'lsgan'  # [vanilla| lsgan | wgangp]
    pool_size: int = 50
    lr_policy: str = 'linear'  # [linear | step | plateau | cosine]
    lr_decay_iters: int = 50

    isTrain: bool = True