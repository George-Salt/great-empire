import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
import jinja2


TASKS_INFO = {
	"wnot": {
		"topic": "Какой нации принадлежит?",
		"question": "Танк какой нации изображен на картинке?",
		"numbers": {
			"1": {
				"difficulty": "Средняя",
				"image": "M36 (Япония).png",
				"answers": {
					"1": {
						"name": "СССР",
						"is_valid": False
					},
					"2": {
						"name": "Япония",
						"is_valid": True
					},
					"3": {
						"name": "США",
						"is_valid": False
					},
					"4": {
						"name": "Китай",
						"is_valid": False
					}
				},
				"solution": "На картинке изображен танк M36 (自衛隊) - является самоходным орудием в ветке исследований техники Японии.",
			},
			"2": {
				"difficulty": "Средняя",
				"image": "M4A2 (СССР).png",
				"answers": {
					"1": {
						"name": "США",
						"is_valid": False
					},
					"2": {
						"name": "Британия",
						"is_valid": False
					},
					"3": {
						"name": "Швеция",
						"is_valid": False
					},
					"4": {
						"name": "СССР",
						"is_valid": True
					}
				},
				"solution": "На картинке изображен «М-Четвёртый» («Эмча», Medium Tank M4A2 (76) W Sherman) - советская модификация M4 Sherman времен Второй Мировой.",
			},
			"3": {
				"difficulty": "Сложная",
				"image": "Т-62 545 (Китай).png",
				"answers": {
					"1": {
						"name": "Япония",
						"is_valid": False
					},
					"2": {
						"name": "СССР",
						"is_valid": False
					},
					"3": {
						"name": "США",
						"is_valid": False
					},
					"4": {
						"name": "Китай",
						"is_valid": True
					}
				},
				"solution": "На картинке изображен танк Т-62 №545 - он произвёл большое впечатление для китайских военных, в результате чего была активизирована программа «122» по созданию современного китайского танка.",
			},
			"4": {
				"difficulty": "Легкая",
				"image": "ЗСУ-57-2.png",
				"answers": {
					"1": {
						"name": "Израиль",
						"is_valid": False
					},
					"2": {
						"name": "СССР",
						"is_valid": True
					},
					"3": {
						"name": "Германия",
						"is_valid": False
					},
					"4": {
						"name": "Китай",
						"is_valid": False
					}
				},
				"solution": "На картинке изображена ЗСУ-57-2 - советская зенитная самоходная установка послевоенного периода, разработанная в 1947–1950 годах.",
			},
			"5": {
				"difficulty": "Средняя",
				"image": "QF 3.7 Ram.png",
				"answers": {
					"1": {
						"name": "США",
						"is_valid": False
					},
					"2": {
						"name": "Франция",
						"is_valid": False
					},
					"3": {
						"name": "Италия",
						"is_valid": False
					},
					"4": {
						"name": "Британия",
						"is_valid": True
					}
				},
				"solution": "На картинке изображена OQF 3.7-inch AA on Ram Mounting - британская самоходная артиллерийская установка разработанная путем установки зенитной пушки OQF 3.7-inch Mk.II на шасси легкого танка M4A5 Ram II.",
			},
			"6": {
				"difficulty": "Средняя",
				"image": "Toldi IIA.png",
				"answers": {
					"1": {
						"name": "Швеция",
						"is_valid": False
					},
					"2": {
						"name": "Германия",
						"is_valid": False
					},
					"3": {
						"name": "Италия",
						"is_valid": True
					},
					"4": {
						"name": "Франция",
						"is_valid": False
					}
				},
				"solution": "На картинке изображен Toldi IIA - венгерский лёгкий танк времён Второй Мировой войны.",
			},
		},
	},
	"wkot": {
		"topic": "Что за танк?",
		"question": "Какой танк изображен на картинке?",
		"numbers": {
			"1": {
				"difficulty": "Средняя",
				"image": "Т-60.png",
				"answers": {
					"1": {
						"name": "Т-70",
						"is_valid": False
					},
					"2": {
						"name": "Т-44",
						"is_valid": False
					},
					"3": {
						"name": "Т-60",
						"is_valid": True
					},
					"4": {
						"name": "Т-26",
						"is_valid": False
					}
				},
				"solution": "На картинке изображен Т-60 - советский легкий танк периода Второй Мировой.",
			},
		},
	},
}


def get_filled_footer():
	return f"""\
	<footer>
		<div class="column left-column">
			<h2>Разделы&nbsp;сайта</h2>
			<a href="blog/trainings/">Тесты&nbsp;для&nbsp;танкистов</a>
			<a href="about/people/">Состав&nbsp;полка</a>
			<a href="blog/articles/">Полезные&nbsp;статьи</a>
		</div>

		<h1>Великая Империя</h1>
		
		<div class="column right-column">
			<h2>Разработка</h2>
			<a href="https://george-salt.github.io/home/">Жора Соляник</a>
		</div>
	</footer>"""


def render_task_page(task_template: jinja2.Template, id, topic, question, difficulty, answers, solution, path, image=None):
	rendered_page = task_template.render(
		id=id,
		topic=topic,
		difficulty=difficulty,
		image=f"../../../../static/imgs/tanks/{image}",
		question=question,
		answers=answers,
		solution=solution
	)

	with open(f"../blog/trainings/{path}/index.html", "w", encoding="utf8") as file:
		file.write(rendered_page)


def render_all_tasks_pages(task_template: jinja2.Template):
	for task_type, task_type_params in TASKS_INFO.items():
		os.makedirs(f"../blog/trainings/{task_type}", exist_ok=True)
		for number_id, number_params in task_type_params["numbers"].items():
			os.makedirs(f"../blog/trainings/{task_type}/{number_id}", exist_ok=True)
			render_task_page(
				task_template,
				number_id,
				task_type_params["topic"],
				task_type_params["question"],
				number_params["difficulty"],
				number_params["answers"],
				number_params["solution"],
				f"{task_type}/{number_id}",
				number_params["image"]
			)


if __name__ == "__main__":
	env = Environment(
		loader=FileSystemLoader("./templates"),
		autoescape=select_autoescape(["html"])
	)
	task_template = env.get_template("task.html")

	render_all_tasks_pages(task_template)
