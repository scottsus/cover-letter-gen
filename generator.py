import os
from openai import OpenAI
from typing import Iterator

class Generator:
    def __init__(self):
        self.model = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
        )

    def generate_cover_letter(self) -> Iterator[str]:
        try:
            resume_contents = self.get_resume()
            job_desc = self.get_job_desc()
            example = self.get_example()

            if not resume_contents:
                raise ValueError('Resume contents are empty')
            if not job_desc:
                raise ValueError('Job description is empty')
            if not example:
                raise ValueError('Example is empty')
            
            contents = (
                'Here are a few examples of great cover letters:\n\n'
                f'{example}\n\n'
                'These are your actual experiences, so feel free to reuse these in your next cover letter.\n'
                
                'Given the job description:\n\n'
                f'{job_desc}\n\n'
                
                'Use this resume to help craft the cover letter:\n\n'
                f'{resume_contents}\n\n'
            )
            
            stream = self.model.chat.completions.create(
                model='gpt-4-1106-preview',
                messages=[
                    {
                        'role': 'system',
                        'content': (
                            'You are applying for a job as a software engineer. '
                            'Write a short, introduction followed by a meaningful set of 5-6 bullet points explaining why, given your background, you would want to work for the company, '
                            'and why you would be a good fit for the role. '
                            'In the introduction, include the position and role number. '
                            'Each bullet should be concise, intelligent, and use a humble tone similar to founders & investors on Twitter. '
                            'Include links encased in square brackets to reference your project. '
                            'End the letter with a strong reason as to why you are excited to join them. '
                            'You should use some (mainly focusing on work experiences, startups, and research projects) '
                            'information from the resume to address the points given in the job description. '
                        )
                    },
                    {
                        'role': 'user',
                        'content': contents
                    }
                ],
                stream=True,
                response_format={ 'type': 'text'}
            )

            for chunk in stream:
                choice = chunk.choices[0]
                if choice.finish_reason == 'stop':
                    return
                
                yield choice.delta.content or ''
        except KeyboardInterrupt:
            return
        except Exception as e:
            yield f'Error: {e}'
    
    def get_resume(self) -> str:
        with open('resume.md', 'r') as f:
            return f.read()
    
    def get_job_desc(self) -> str:
        with open('job_desc.md', 'r') as f:
            return f.read()
    
    def get_example(self) -> str:
        with open('example.md', 'r') as f:
            return f.read()
    