from IPython.display import display
from Main import RandomDerivative, RandomIntegral, check

class Trainer:
    @staticmethod
    def practice_derivatives(num):
        for i in range(num):
            display(f'Problem {i + 1}:')

        RandomDerivative.init()
        e = RandomDerivative.generate()
        display(RandomDerivative.equation(e))
        display(RandomDerivative.question())

        answer = input('Enter your answer: \n')
        print(f'Your answer: {answer}')

        correct_answer = RandomDerivative.answer(e)
        print('Correct!' if check(answer, correct_answer) else 'Incorrect!')
        display(correct_answer)

    @staticmethod
    def practice_integrals(num):
        for i in range(num):
            display(f'Problem {i + 1}:')

        RandomIntegral.init()
        e = RandomIntegral.generate()
        display(RandomIntegral.equation(e))
        display(RandomIntegral.question())

        answer = input('Enter your answer: \n')
        print(f'Your answer: {answer}')

        correct_answer = RandomIntegral.answer(e)
        print('Correct!' if check(answer, correct_answer) else 'Incorrect!')
        display(correct_answer)