from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
  waiting_for_mpg = State()
  waiting_for_m = State()
  