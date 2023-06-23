#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


# 一個 Employee 的類別, 用來作 DTO (Data Transfer Object) 使用
class Employee:

    def __init__(self, id_='', first_name='', last_name='', dept_id='',
                 hire_date=None, termination_date=None, wage=0.0,
                 age=0, sex=False):
        self.id_ = id_
        self.first_name = first_name
        self.last_name = last_name
        self.dept_id = dept_id
        self.hire_date = hire_date
        self.termination_date = termination_date
        self.wage = wage
        self.age = age
        self.sex = sex
