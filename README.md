# プロジェクトのPlaybooks
## プロジェクト構造

```
ansible-playbooks
├ common_playbooks (submodule)
└ project_playbooks
```

# project_playbooks
project_playbooks は、アプリ間を問わず、共通のディレクトリ名とする。

### forami-wt-dev-ansibleのAMI作成
 - Ansible 実行 option --env_ : 環境タグを指定

```[ec2-user@ip-10-141-156-109 project_playbooks]$ ./play.py --env=development forami-wt-dev-ansible.yml```

 - 発生したインスタンスにwt-dev.pemキーを入れます。(管理者にご連絡ください)
 
```PATH: /home/ec2-user/.ssh```
 
 - AMIイメージ 作成 option --instance-id: 発生したインスタンスID　--name: AMI名   (AMIのネーミングルール: ami-wt-dev-ansible-YYYYMMDD-NN)

```aws ec2 create-image --instance-id <インスタンスID> --no-reboot --name <AMIの名前>```

### ansibleインスタンス作成
 - Ansible 実行 option --env_ : 環境タグを指定

```[ec2-user@ip-10-141-156-109 project_playbooks]$ ./play.py --env=development ansible.yml```

### forami-wt-dev-bastionのAMI作成
 - Ansible 実行 option --env_ : 環境タグを指定

```[ec2-user@ip-10-141-156-109 project_playbooks]$ ./play.py --env=development forami-wt-dev-bastion.yml```

 - AMIイメージ 作成 option --instance-id: 発生したインスタンスID　--name: AMI名   (AMIのネーミングルール: ami-wt-dev-bastion-YYYYMMDD-NN)

```aws ec2 create-image --instance-id <インスタンスID> --no-reboot --name <AMIの名前>```

### bastionインスタンス作成
 - Ansible 実行 option --env_ : 環境タグを指定

```[ec2-user@ip-10-141-156-109 project_playbooks]$ ./play.py --env=development bastion.yml```


---

# common_playbooks
common_playbooks/roles 配下はモジュールを管理。

