# reallife : 项目级别
我们开始做一个升级, 0.2 为稳定本地版, 0.3 要做成client 和server 的配合, 新拉一个分支来做
快捷调度生活,将快捷指令系统构成的真实人生系统编写为以代码为主的模式, 为真实人生项目提供标准化工具

## 常规操作

### 导出环境
```
uv export --format requirements-txt > requirements.txt
```
### 更新文档
```
mkdocs serve # 预览
mkdocs gh-deploy -d ../.temp # 同步到github网站
```

### 发布
```
uv build
uv publish
```

### 运行测试并同步到测试服务
```
bash run_test.sh
```

### 

@pytest.mark.slow
pytest -m slow # 运行带有 `slow` 标记的测试
pytest -m "not slow"  # 运行不带有 `slow` 标记的测试
pytest test_example.py::test_add

运行失败的测试 | pytest --lf 
查看详细输出  | pytest -v 
