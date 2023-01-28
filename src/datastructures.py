
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = [{"first_name": "Sandra", "id": 1, "age": 34, "lucky_numbers": [7, 8, 19]}]

    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        member['id'] = self._generateId()
        self._members.append(member)
        return member

    def delete_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member['id'] == id:
                self._members.remove(member)

    def update_member(self, id, new_member):
        for index, member in enumerate(self._members):
            if member['id'] == id:
                new_member['id'] = member['id']
                self._members[index] = new_member

    def get_member(self, id):
        for member in self._members:
            if member['id'] == id:
                return member
        return {'message': 'Member not found'}
        
    def get_all_members(self):
        return self._members

# this class could be used to create members programmatically
class Member:
    def __init__(self, first_name, last_name, age, lucky_numbers):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.lucky_numbers = lucky_numbers