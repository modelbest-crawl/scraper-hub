.PHONY: install install-project run new-project test test-owner test-project test-packages test-smoke lint lint-owner format registry health add-member offboard-member

# ——— 安装 ———

install:
	pip install -e .
	pip install -r requirements-base.txt
	pip install pre-commit && pre-commit install

install-project:
	pip install -r projects/$(owner)/$(name)/requirements.txt

# ——— 运行 ———

run:
	python -m projects.$(owner).$(name).scraper

# ——— 新建项目 ———

new-project:
	@bash scripts/new_project.sh $(owner) $(name)

# ——— 团队管理 ———

add-member:
	@bash scripts/add_member.sh $(name) $(github)

offboard-member:
	@bash scripts/offboard_member.sh $(name)

# ——— 测试 ———

test:
	pytest projects/ packages/ -m "not smoke" --tb=short -q

test-owner:
	pytest projects/$(owner)/ -m "not smoke" --tb=short -q

test-project:
	pytest projects/$(owner)/$(name)/tests/ --tb=short -q

test-packages:
	pytest packages/ --tb=short -q

test-smoke:
	pytest projects/ -m smoke --tb=short -q

# ——— Lint & Format ———

lint:
	ruff check packages/ projects/

lint-owner:
	ruff check projects/$(owner)/

format:
	ruff format packages/ projects/

# ——— 工具 ———

registry:
	python scripts/generate_registry.py

health:
	python scripts/check_health.py
