"""Parse models in c2sketch's own concrete syntax"""
from __future__  import annotations

from typing import Type
from dataclasses import dataclass
from c2sketch.models import (ModelID, Node, Import, Attribute, Constraint, Actor, ActorGroup, ActorMember, ActorLocation, Location, LocationGroup, LocationMember, InformationSpace,
                               InformationSpaceRequirement, InformationSpaceBinding, FieldMode, AgeLimit, KeyLimit,
                               Record, PrimitiveTypeID, RecordType, RecordTypeField, Model, Problem,
                               Task, TaskDefinition, TaskInstance, ImplicitTask, ImplicitTaskInstance, TaskReference, Trigger)

import lark, lark.indenter, lark.lexer, lark.visitors
import re
import pathlib

@dataclass
class C2SSyntaxError(Exception):
    msg: str
    lineno: int | None
    offset: int | None
    model: str | None

@dataclass
class C2SLexError(Exception):
    msg: str
    lineno: int | None
    offset: int | None

class C2SLexer(lark.lexer.Lexer):
    """Custom lexer to be able to handle indenting and multi-line free text rules."""
    def __init__(self, lexer_conf):
        ...

    def lex(self, data:str):
        position = 0
        line = 0
        column = 0

        # Tracking state to inject INDENT / DEDENT virtual tokens
        line_start = True
        indent_width = 0

        # Tracking the start of attribute definitions for the
        # 'bare lines' layout rule
        attribute_line = None
        read_bare_lines = False

        rules: list[tuple[str,re.Pattern]] = [
            # Keywords
            ('IMPORT',re.compile(r'import')),
            ('ACTOR',re.compile(r'actor')),
            ('MEMBER',re.compile(r'member')),
            ('GROUP',re.compile(r'group')),
            ('LOCATION',re.compile(r'location')),
            ('AT_LOCATION',re.compile(r'at-location')),
            ('TASK_DEF',re.compile(r'task-def')),
            ('TASK_INSTANCE',re.compile(r'task-instance')),
            ('TASK_REF',re.compile(r'task-ref')),
            ('TASK',re.compile(r'task')),
            ('INFO_REQ',re.compile(r'info-req')),
            ('INFO_SPACE',re.compile(r'info-space')),
            ('TRIGGER',re.compile(r'trigger')),
            ('RECORD_TYPE',re.compile(r'record-type')),
            ('RECORD',re.compile(r'record')),
            ('FIELD_MODE',re.compile(r'field-mode')),
            ('FIELD_MODE_VALUE',re.compile(r'key|first|last|min|max')),
            ('FIELD',re.compile(r'field')),
            ('AGE_LIMIT',re.compile(r'age-limit')),
            ('KEY_LIMIT',re.compile(r'key-limit')),
            # Structural characters
            ('COLON',re.compile(r':')),
            ('COMMA',re.compile(r',')),
            ('EQUAL',re.compile(r'=')),
            ('LSQB',re.compile(r'\[')),
            ('RSQB',re.compile(r'\]')),
            ('LBRACE',re.compile(r'{')),
            ('RBRACE',re.compile(r'}')),
            ('IS_RW',re.compile(r'<->')),
            ('IS_R',re.compile(r'<-')),
            ('IS_W',re.compile(r'->')),
            # Identifiers
            ('ATTRIBUTE_ID',re.compile(r'@[a-zA-Z0-9_\-]+')),
            ('CONSTRAINT_ID',re.compile(r'![a-zA-Z0-9_\-]+')),
            ('SIMPLE_ID',re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')),
            ('DOTTED_ID',re.compile(r'[a-zA-Z_][a-zA-Z0-9_\.]*(@[a-zA-Z0-9_\.]+)?')),
            # Literals
            ('SIGNED_INT',re.compile(r'[+\-]?[0-9]+')), # Adapted form common.lark
            ('ESCAPED_STRING',re.compile(r'".*?(?<!\\)(\\\\)*?"')), # Adapted from common.lark
            # Whitespace
            ('WS',re.compile(r'[ \t]+')),
            ('NL',re.compile(r'\r?\n')),
            ('COMMENT',re.compile(r'#[^\r\n]*'))
        ]

        bare_line_rule = re.compile(r'[^\r\n]+')
        empty_line_rule = re.compile(r'[ \t]*(#[^\r\n]*)?\r?\n')

        while position < len(data):
            
            longest_match = None

            for token_name, pattern in rules:
                match = pattern.match(data,position)
                if match and (longest_match is None or match.end() > longest_match[1].end()):
                    longest_match = (token_name,match)
                
            if longest_match is not None:
                
                token_name = longest_match[0]
                token_string = longest_match[1].group()
                position = longest_match[1].end()

                # Track attribute definitions
                if token_name == 'ATTRIBUTE_ID':
                    attribute_line = line

                # At the beginning of a line, check if the indent width changes
                if line_start:
                    if token_name == 'WS':
                        new_indent_width = len(token_string.replace('\t','    '))
                    else:
                        new_indent_width = 0

                    empty_line = empty_line_rule.match(data,longest_match[1].start()) is not None 
                    
                    if not empty_line:
                        #Adjust indentation, but ignore empty lines
                        if new_indent_width > indent_width:
                            #For each 4 spaces emit an indent token
                            for _ in range((new_indent_width - indent_width) // 4):
                                yield lark.lexer.Token('INDENT', '', position, line, column)
                            # Apply the bare lines rule for (multi-line) attribute specifications
                            if attribute_line == (line - 1):
                                read_bare_lines = True
                        elif new_indent_width < indent_width:
                            #For each 4 spaces emit a dedent token
                            for _ in range((indent_width - new_indent_width) // 4):
                                yield lark.lexer.Token('DEDENT', '', position, line, column)
                            read_bare_lines = False

                        indent_width = new_indent_width
                    
                    line_start = False

                # Ignore whitespace and comments
                if token_name not in ['WS','COMMENT']: 
                    yield lark.lexer.Token(token_name, token_string, position, line, column)

                # Reset line start after a new line token
                if token_name == 'NL':
                    line += 1
                    column = 0
                    line_start = True
                else:
                    # Advance column counter
                    column += len(token_string)
                
                # Read everything until the end of the line or string
                if (not line_start) and read_bare_lines:
                    match = bare_line_rule.match(data, position)
                    if match:
                        position = match.end()
                        token_string =  match.group()
                        column += len(token_string)
                        yield lark.lexer.Token('BARE_LINE', token_string, position, line, column)     
            else:
                raise C2SLexError(f'unexpected character \'{data[position]}\' at position {column} on line {line}', line, column)

        #Add final newline and dedents if we end the input while still indented
        if indent_width > 0:
            yield lark.lexer.Token('NL', '\n', position, line, column)
            #For each 4 spaces emit a dedent token
            for _ in range(indent_width // 4):
                yield lark.lexer.Token('DEDENT', '', position, line, column)
        
        #Always emit a final newline
        yield lark.lexer.Token('NL', '\n', position, line, column)

c2s_grammar = '''
model : NL* ((import_ref | attribute | actor | location | task | task_definition | task_instance | info_space | record_type))*

import_ref: IMPORT id NL+

attribute: ATTRIBUTE_ID ((literal NL+) | (":" NL+ INDENT (BARE_LINE NL+)+ DEDENT NL*))
constraint: CONSTRAINT_ID id NL+

?id: SIMPLE_ID | DOTTED_ID
?literal: ESCAPED_STRING | SIGNED_INT

actor: ACTOR SIMPLE_ID (NL+ | (":" NL+ INDENT actor_body_node+ DEDENT NL*))
?actor_body_node: attribute | constraint | actor_member | actor_group | actor_location
actor_member: MEMBER id NL+
actor_group: GROUP id NL+
actor_location: AT_LOCATION id NL+

location: LOCATION SIMPLE_ID (NL+ | (":" NL+ INDENT location_body_node+ DEDENT NL*))
?location_body_node: attribute | location_member | location_group
location_member: MEMBER id NL+
location_group: GROUP id NL+

task: TASK SIMPLE_ID  (NL+ | (":" NL+ INDENT task_body_node+ DEDENT NL*))
?task_body_node: attribute | constraint | task | task_definition | task_instance | task_reference | task_trigger | info_req

task_definition: TASK_DEF SIMPLE_ID task_definition_type (NL+ | (":" NL+ INDENT task_definition_body_node+ DEDENT NL*))
task_definition_type: "[" id "]"
?task_definition_body_node: attribute | constraint | task | task_definition | task_instance | task_reference | task_trigger | info_req | info_space

task_instance: TASK_INSTANCE SIMPLE_ID record_literal (NL+ | (":" NL+ INDENT task_instance_body_node+ DEDENT NL*))
?task_instance_body_node: attribute | constraint | info_req_binding | task_instance | task_trigger

task_reference: TASK_REF id record_literal? NL+
task_trigger: TRIGGER SIMPLE_ID NL+

info_req: INFO_REQ info_direction? SIMPLE_ID info_type? info_binding? NL+
info_type: "[" id "]"
info_direction: IS_RW | IS_R | IS_W
info_binding: "=" id

info_req_binding: INFO_REQ SIMPLE_ID "=" id NL+

info_space: INFO_SPACE SIMPLE_ID info_type? (NL+ | (":" NL+ INDENT info_space_body_node+ DEDENT NL*))
?info_space_body_node: attribute | constraint | field_mode | age_limit | key_limit | record

field_mode: FIELD_MODE SIMPLE_ID FIELD_MODE_VALUE NL+
key_limit: KEY_LIMIT SIGNED_INT NL+
age_limit: AGE_LIMIT SIGNED_INT NL+

record: RECORD record_literal NL+
record_literal: "{" (SIMPLE_ID "=" literal ("," SIMPLE_ID "=" literal)*)? "}"

record_type: RECORD_TYPE SIMPLE_ID (NL+ | (":" NL+ INDENT record_type_body_node+ DEDENT NL*))
?record_type_body_node: attribute | record_type_field

record_type_field: FIELD SIMPLE_ID field_type? NL+
?field_type: "[" id "]"

%declare WS NL BARE_LINE INDENT DEDENT
%declare ATTRIBUTE_ID CONSTRAINT_ID SIMPLE_ID DOTTED_ID ESCAPED_STRING SIGNED_INT
%declare IMPORT ACTOR MEMBER GROUP LOCATION AT_LOCATION TASK TASK_DEF TRIGGER TASK_INSTANCE TASK_REF
%declare INFO_REQ IS_RW IS_R IS_W INFO_SPACE RECORD
%declare RECORD_TYPE FIELD FIELD_MODE FIELD_MODE_VALUE AGE_LIMIT KEY_LIMIT
'''

#Mapping between grammar rules and model node types

c2s_node_mapping = {
    Model:'model',
    Import: 'import_ref',
    Attribute: 'attribute',
    Constraint: 'constraint',
    Actor: 'actor',
    ActorMember: 'actor_member',
    ActorGroup: 'actor_group',
    ActorLocation: 'actor_location',
    Location: 'location',
    LocationMember: 'location_member',
    LocationGroup: 'location_group',
    Task: 'task',
    TaskReference: 'task_reference',
    Trigger: 'task_trigger',
    InformationSpaceRequirement: 'info_req',
    TaskDefinition: 'task_definition',
    TaskInstance: 'task_instance',
    InformationSpaceBinding: 'info_req_binding',
    InformationSpace: 'info_space',
    FieldMode: 'field_mode',
    KeyLimit: 'key_limit',
    AgeLimit: 'age_limit',
    Record: 'record',
    RecordType: 'record_type',
    RecordTypeField: 'record_type_field',
}

#Singleton parser object
c2s_parser = lark.Lark(c2s_grammar, start= list(c2s_node_mapping.values()), lexer=C2SLexer)

class C2SNodeBuilder(lark.visitors.Interpreter):
   
    _parent_stack: list[Node]
    _sequence_stack: list[dict[str,int]]

    def __init__(self, model_id: str):
        self._model_id = model_id
        self._parent_stack = []
        self._sequence_stack = []
        super().__init__()

    def model(self, tree: lark.Tree[lark.Token]):
        model = Model(self._model_id)
        
        self._parent_stack.append(model)
        self._sequence_stack.append({})

        items = self.visit_children(tree)
        model.nodes = [node for node in items if isinstance(node,Node)]
       
        self._parent_stack.pop()
        self._sequence_stack.pop()

        return model
    
    def import_ref(self, tree: lark.Tree[lark.Token]):
        import_token = tree.children[0]
        reference_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(import_token, lark.Token)
        assert isinstance(reference_token, lark.Token)
        assert isinstance(parent,Model) or parent is None
        return Import(reference_token.strip(),parent,import_token.line,import_token.line)
    
    def attribute(self, tree: lark.Tree[lark.Token]):
        attribute_token = tree.children[0]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(attribute_token, lark.Token)

        source_start = attribute_token.line
        source_end = attribute_token.line
        
        name = attribute_token[1:]
        lines = []
        for token in tree.children[1:]:
            assert isinstance(token,lark.Token)
            if token.type == 'ESCAPED_STRING':
                lines.append(token[1:-1]) #TODO: Unescape quotes
            elif token.type  == 'BARE_LINE':
                source_end = token.line
                lines.append(str(token))
        
        value = ('\n'.join(lines)).strip()

        return Attribute(name,value,parent,source_start,source_end)
    
    def constraint(self, tree: lark.Tree[lark.Token]):
        constraint_token = tree.children[0]
        value_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(constraint_token,lark.Token)
        assert isinstance(value_token,lark.Token)
        name = constraint_token[1:]
        value = value_token.strip()
        return Constraint(name,value,parent,constraint_token.line,constraint_token.line)
    
    def actor(self, tree: lark.Tree[lark.Token]):
        actor_token = tree.children[0]
        name_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(actor_token,lark.Token)
        assert isinstance(name_token,lark.Token)
        assert isinstance(parent,Model) or parent is None

        name = str(name_token)
        actor = Actor(name,parent)
        self._parent_stack.append(actor)

        for child in tree.children[2:]:
            if not isinstance(child,lark.Tree):
                continue
            
            node = self.visit(child)
            assert isinstance(node,Node)
            actor.nodes.append(node)
          
        actor.source_start = actor_token.line
        actor.source_end = actor.nodes[-1].source_end if actor.nodes else actor_token.line
       
        self._parent_stack.pop()
        return actor
    
    def actor_member(self, tree: lark.Tree[lark.Token]):
        member_token = tree.children[0]
        actor_id_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(member_token,lark.Token)
        assert isinstance(actor_id_token,lark.Token)
        assert isinstance(parent,Actor) or parent is None
        
        actor_id = actor_id_token.strip()
        return ActorMember(actor_id,parent,member_token.line,member_token.line)
    
    def actor_group(self, tree: lark.Tree[lark.Token]):
        group_token = tree.children[0]
        group_id_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(group_token,lark.Token)
        assert isinstance(group_id_token,lark.Token)
        assert isinstance(parent,Actor) or parent is None

        group_id = group_id_token.strip()
        return ActorGroup(group_id,parent,group_token.line,group_token.line)

    def actor_location(self, tree: lark.Tree[lark.Token]):
        location_token = tree.children[0]
        location_id_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(location_token,lark.Token)
        assert isinstance(location_id_token,lark.Token)
        assert isinstance(parent,Actor) or parent is None
        
        location_id = location_id_token.strip()
        return ActorLocation(location_id,parent,location_token.line,location_token.line)

    def location(self, tree: lark.Tree[lark.Token]):
        location_token = tree.children[0]
        name_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(location_token,lark.Token)
        assert isinstance(parent,Model) or parent is None
        
        name = str(name_token)
        location = Location(name,parent)

        self._parent_stack.append(location)

        for child in tree.children[2:]:
            if not isinstance(child,lark.Tree):
                continue
            
            node = self.visit(child)
            assert isinstance(node,Node)
            location.nodes.append(node)

        location.source_start = location_token.line
        location.source_end = location.nodes[-1].source_end if location.nodes else location_token.line
       
        self._parent_stack.pop()
        return location

    def location_group(self, tree: lark.Tree[lark.Token]):
        group_token = tree.children[0]
        group_id_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(group_token,lark.Token)
        assert isinstance(group_id_token,lark.Token)
        assert isinstance(parent,Location) or parent is None

        group_id = group_id_token.strip()

        return LocationGroup(group_id,parent,group_token.line,group_token.line)

    def location_member(self, tree: lark.Tree[lark.Token]):
        member_token = tree.children[0]
        location_id_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(member_token,lark.Token)
        assert isinstance(location_id_token,lark.Token)
        assert isinstance(parent,Location) or parent is None
        
        location_id = location_id_token.strip()
        return LocationMember(location_id,parent,member_token.line,member_token.line)
    
    def task(self, tree: lark.Tree[lark.Token]):
        task_token = tree.children[0]
        name_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(task_token,lark.Token)
        assert isinstance(name_token,lark.Token)
        assert isinstance(parent,Model) or isinstance(parent,Task) or isinstance(parent,TaskDefinition) or parent is None
        
        name = str(name_token)
        task = Task(name,parent)

        self._parent_stack.append(task)
        self._sequence_stack.append({})

        for child in tree.children[2:]:
            if not isinstance(child,lark.Tree):
                continue
            
            node = self.visit(child)
            assert isinstance(node,Node)
            task.nodes.append(node)

        task.source_start = task_token.line
        task.source_end = task.nodes[-1].source_end if task.nodes else task_token.line
       
        self._parent_stack.pop()
        self._sequence_stack.pop()

        return task
    
    def task_reference(self, tree: lark.Tree[lark.Token]):
        task_ref_token = tree.children[0]
        reference_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(task_ref_token,lark.Token)
        assert isinstance(reference_token,lark.Token)
        assert isinstance(parent,Task) or isinstance(parent,TaskDefinition) or parent is None

        reference = reference_token.strip()
        parameter = None

        if len(tree.children) > 2 and isinstance(tree.children[2],lark.Tree):
            parameter = self.visit(tree.children[2])
            assert isinstance(parameter,dict)

        return TaskReference(reference,parameter,parent,task_ref_token.line,task_ref_token.line)
    
    def task_trigger(self,tree: lark.Tree[lark.Token]):
        trigger_token = tree.children[0]
        reference_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(trigger_token,lark.Token)
        assert isinstance(reference_token,lark.Token)
        assert isinstance(parent,Task) or isinstance(parent,TaskDefinition) or isinstance(parent,TaskInstance) or parent is None

        reference = reference_token.strip()
        return Trigger(reference,parent,trigger_token.line,trigger_token.line)

    def info_req(self, tree: lark.Tree[lark.Token]):

        req_token = tree.children[0]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(req_token,lark.Token)
        assert isinstance(parent,Task) or isinstance(parent,TaskDefinition) or parent is None

        items = [child for child in tree.children[1:]]
        
        read, write = True, True
        type = None
        binding = None

        if isinstance(items[0],lark.Tree) and items[0].data == 'info_direction':
            match items[0].children[0]:
                case '->':
                    read, write = False, True
                case '<-':
                    read, write = True, False
            items.pop(0)
        
        name = str(items.pop(0))
        
        if isinstance(items[0],lark.Tree) and items[0].data == 'info_type':
            type_node = items[0]
            type = str(type_node.children[0])
            items.pop(0)
        
        if isinstance(items[0],lark.Tree) and items[0].data == 'info_binding':
            binding_node = items[0]
            binding = str(binding_node.children[0])
            items.pop(0)

        return InformationSpaceRequirement(name, type, read, write, binding, parent, req_token.line, req_token.line)
    
    def task_definition(self, tree: lark.Tree[lark.Token]):

        task_def_token = tree.children[0]
        name_token = tree.children[1]
        parameter_type_tree = tree.children[2]
        parent = self._parent_stack[-1] if self._parent_stack else None
        
        assert isinstance(task_def_token,lark.Token)
        assert isinstance(name_token,lark.Token)
        assert isinstance(parameter_type_tree,lark.Tree)
        assert isinstance(parent,Model) or isinstance(parent,Task) or isinstance(parent,TaskDefinition) or parent is None
        
        name = str(name_token)
        parameter_type = str(parameter_type_tree.children[0])
        task_def = TaskDefinition(name,parameter_type,parent)

        self._parent_stack.append(task_def)
        self._sequence_stack.append({})

        for child in tree.children[3:]:
            if not isinstance(child,lark.Tree):
                continue
            
            node = self.visit(child)
            assert isinstance(node,Node)
            task_def.nodes.append(node)

        task_def.source_start = task_def_token.line
        task_def.source_end = task_def.nodes[-1].source_end if task_def.nodes else task_def_token.line
       
        self._parent_stack.pop()
        self._sequence_stack.pop()

        return task_def
    
    def task_instance(self, tree: lark.Tree[lark.Token]):

        task_instance_token = tree.children[0]
        name_token = tree.children[1]
        parameter_tree = tree.children[2]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(task_instance_token,lark.Token)
        assert isinstance(name_token,lark.Token)
        assert isinstance(parameter_tree,lark.Tree)
        assert isinstance(parent,Model) or isinstance(parent,Task) or isinstance(parent,TaskDefinition) \
            or isinstance(parent,TaskInstance) or isinstance(parent,ImplicitTask) or isinstance(parent,ImplicitTaskInstance) \
            or parent is None
        

        name = str(name_token)
        parameter = self.visit(parameter_tree)

        assert isinstance(parameter, dict)

        #Lookup next sequence number
        if self._sequence_stack:
            if name not in self._sequence_stack[-1]:
                sequence = 1
            else:
                sequence = self._sequence_stack[-1][name] + 1
            self._sequence_stack[-1][name] = sequence
        else:
            sequence = 1
        
        task_instance = TaskInstance(name,sequence,parameter,parent)
        self._parent_stack.append(task_instance)
        self._sequence_stack.append({})

        for child in tree.children[3:]:
            if not isinstance(child,lark.Tree):
                continue
            
            node = self.visit(child)
            assert isinstance(node,Node)
            task_instance.nodes.append(node)

        task_instance.source_start = task_instance_token.line
        task_instance.source_end = task_instance.nodes[-1].source_end if task_instance.nodes else task_instance_token.line
       
        self._parent_stack.pop()
        self._sequence_stack.pop()

        return task_instance
    
    def info_req_binding(self, tree: lark.Tree[lark.Token]):
        info_req_token = tree.children[0]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(info_req_token,lark.Token)
        assert isinstance(parent,TaskInstance) or parent is None

        name = str(tree.children[1])
        binding = str(tree.children[2])

        return InformationSpaceBinding(name,binding,parent,info_req_token.line,info_req_token.line)
    
    def info_space(self, tree: lark.Tree[lark.Token]):
        info_space_token = tree.children[0]
        name_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None
        assert isinstance(info_space_token,lark.Token)
        assert isinstance(name_token,lark.Token)
        assert isinstance(parent,Model) or isinstance(parent,InformationSpace) or parent is None

        name = str(name_token)
        ifs = InformationSpace(name,None,parent)

        self._parent_stack.append(ifs)
        self._sequence_stack.append({})

        for child in tree.children[2:]:
            if not isinstance(child,lark.Tree):
                continue
            
            if child.data == 'info_type':
                type_token = child.children[0]
                assert isinstance(type_token,lark.Token)
                ifs.type = str(type_token)
            else:
                node = self.visit(child)
                assert isinstance(node,Node)
                ifs.nodes.append(node)
          
        ifs.source_start = info_space_token.line
        ifs.source_end = ifs.nodes[-1].source_end if ifs.nodes else info_space_token.line
       
        self._parent_stack.pop()
        self._sequence_stack.pop()

        return ifs
 
    def field_mode(self, tree: lark.Tree[lark.Token]):
        mode_token = tree.children[0]
        field_token = tree.children[1]
        value_token = tree.children[2]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(mode_token,lark.Token)
        assert isinstance(field_token,lark.Token)
        assert isinstance(value_token,lark.Token)
        assert isinstance(parent,InformationSpace) or parent is None

        return FieldMode(str(field_token),str(value_token),parent,mode_token.line,mode_token.line)
       
    def key_limit(self, tree: lark.Tree[lark.Token]):
        key_limit_token = tree.children[0]
        value_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(key_limit_token,lark.Token)
        assert isinstance(value_token,lark.Token)
        assert isinstance(parent,InformationSpace) or parent is None

        return KeyLimit(int(value_token.value),parent,key_limit_token.line,key_limit_token.line)

    def age_limit(self, tree: lark.Tree[lark.Token]):
        age_limit_token = tree.children[0]
        value_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(age_limit_token,lark.Token)
        assert isinstance(value_token,lark.Token)
        assert isinstance(parent,InformationSpace) or parent is None

        return AgeLimit(int(value_token.value),parent,age_limit_token.line,age_limit_token.line)

    def record(self, tree: lark.Tree[lark.Token]):
        record_token = tree.children[0]
        fields_tree = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(record_token,lark.Token)
        assert isinstance(fields_tree,lark.Tree)
        assert isinstance(parent,InformationSpace) or parent is None

        fields = self.visit(fields_tree)
        assert isinstance(fields,dict)
        
        if parent is None or (parent.name not in self._sequence_stack[-1]):
            sequence_number= 1
        else:
            sequence_number = self._sequence_stack[-1][parent.name] + 1
        if parent is not None:
            self._sequence_stack[-1][parent.name] = sequence_number
       
        return Record(fields,sequence_number,parent=parent,source_start=record_token.line,source_end=record_token.line)
    
    def record_literal(self, tree: lark.Tree[lark.Token]) -> dict[str,int|str]:
        values = {}
        for i in range(0,len(tree.children),2):
            cur_child = tree.children[i]
            next_child = tree.children[i+1]
            if not isinstance(cur_child,lark.Token) or not isinstance(next_child,lark.Token) :
                continue
            name = str(cur_child)
            if next_child.type == 'SIGNED_INT':
                value = int(next_child.value)
            else:
                value = next_child[1:-1] #TODO properly handle ESCAPED_STRING tokens
            
            values[name] = value

        return values
    
    def record_type(self, tree: lark.Tree[lark.Token]):
        record_type_token = tree.children[0]
        name_token = tree.children[1]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(record_type_token,lark.Token)
        assert isinstance(name_token,lark.Token)
        assert isinstance(parent,Model) or parent is None

        name = str(name_token)
        record_type = RecordType(name,parent)

        self._parent_stack.append(record_type)
        
        for child in tree.children[2:]:
            if not isinstance(child,lark.Tree):
                continue
            
            node = self.visit(child)
            assert isinstance(node,Node)
            record_type.nodes.append(node)

        self._parent_stack.pop()

        record_type.source_start = record_type_token.line
        record_type.source_end = record_type.nodes[-1].source_end if record_type.nodes else record_type_token.line
        
        return record_type

    def record_type_field(self, tree: lark.Tree[lark.Token]):
        field_token = tree.children[0]
        name_token = tree.children[1]
        type_token = tree.children[2]
        parent = self._parent_stack[-1] if self._parent_stack else None

        assert isinstance(field_token,lark.Token)
        assert isinstance(name_token,lark.Token)
        assert isinstance(type_token,lark.Token)
        assert isinstance(parent,RecordType) or parent is None
        
        name = str(name_token)
        type = str(type_token)
        return RecordTypeField(name, type, parent, field_token.line,field_token.line)

def model_node_from_c2s_str(source: str, node_type: Type, model_id = '<input>') -> Node:
   
    rule = c2s_node_mapping[node_type]
    try:
        tree = c2s_parser.parse(source,start=rule)
    except C2SLexError as e:
        raise C2SSyntaxError(f'{e.msg} of {model_id}',e.lineno, e.offset, model_id) from None
    except lark.exceptions.UnexpectedToken as e:  
        raise C2SSyntaxError(f'unexpected {e.token.type} at position {e.column} on line {e.line} of {model_id}', e.line, e.column, model_id) from None
    except lark.exceptions.UnexpectedEOF as e:
        raise C2SSyntaxError(f'unexpected end of file on line {e.line} of {model_id}', e.line, e.column, model_id) from None
    node = C2SNodeBuilder(model_id).visit(tree)
    return node

def model_from_c2s_str(model_id: ModelID, source: str, allow_syntax_errors: bool = False):
    if allow_syntax_errors:
        try:
            model = model_node_from_c2s_str(source, Model, model_id)
        except C2SSyntaxError as e:
            model = Model(model_id)
            model.problems = [Problem(e.msg)]
    else:
        model = model_node_from_c2s_str(source, Model, model_id)
    
    assert isinstance(model,Model)
    model.source = source.splitlines()
    return model

def model_from_c2s_file(model_id: ModelID, path: str | pathlib.Path, allow_syntax_errors: bool = False) -> Model:
    
    if isinstance(path,str):
        path = pathlib.Path(path)

    return model_from_c2s_str(model_id, path.read_text(), allow_syntax_errors)