from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.filters import and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery