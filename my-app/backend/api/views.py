import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class TextEditor(APIView):

    def post(self, request):
        content = request.data.get('content', [])
        commands = request.data.get('commands', [])

        # Ensure content is a list of strings
        if isinstance(content, str):
            content = [content]  # Convert single string content to list
        
        print(f"Original content: {content}")
        print(f"Commands: {commands}")

        # Process commands and get updated content
        processed_content = self.process_commands_in_memory(content, commands)

        # Prepare the response data
        response_data = {
            "received_data": {
                "original_content": content,
                "processed_content": processed_content,
                "command_count": len(commands),
            },
            "message": "Data byla úspěšně zpracována!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def process_commands_in_memory(self, content, commands):
        lineIndex = 0

        for line in commands:
            print(f"Processing command: {line}")
            if line.startswith("removeWord"):
                content = self.process_remove_word(content, line, lineIndex)
            elif line.startswith("addToEnd"):
                content = self.process_add_to_end(content, line, lineIndex)
            elif line.startswith("remove"):
                content = self.process_remove(content, line, lineIndex)
            elif line.startswith("reverse"):
                content = self.process_reverse(content, line, lineIndex)
            elif line.startswith("duplicate"):
                content = self.process_duplicate(content, line, lineIndex)
            elif line.startswith("swapWithNextLine"):
                content = self.process_swap_with_next_line(content, line, lineIndex)
            elif line.startswith("swapWithPreviousLine"):
                content = self.process_swap_with_previous_line(content, line, lineIndex)
            elif line.startswith("removeWhiteSpaces"):
                content = self.process_remove_white_spaces(content, line, lineIndex)
            elif line.startswith("addNewLine"):
                content = self.process_add_new_line(content, line, lineIndex)
            elif line.startswith("writeToConsole"):
                content = self.process_write_to_console(content, line, lineIndex)
            elif line.startswith("replaceWord"):
                content = self.process_replace_word(content, line, lineIndex)
            elif line.startswith("replace"):
                content = self.process_replace(content, line, lineIndex)
            else:
                print(f"Unknown command: {line}")

            # Increase lineIndex for certain commands
            if line.startswith("newLine"):
                lineIndex += 1
            elif content:  # Ensure lineIndex does not exceed content length
                lineIndex = min(lineIndex, len(content) - 1)

        return content

    def process_add_to_end(self, content, command_line, lineIndex):
        match = re.search(r'addToEnd\s+(.+)', command_line)
        if match and 0 <= lineIndex < len(content):
            string_to_add = match.group(1)
            content[lineIndex] += " " + string_to_add
        return content

    def process_remove(self, content, command_line, lineIndex):
        match = re.search(r'remove\s+(\d+)\s+(\d+)', command_line)
        if match and 0 <= lineIndex < len(content):
            try:
                start_index = int(match.group(1))
                num_to_remove = int(match.group(2))
                line = content[lineIndex]

                if 0 <= start_index < len(line):
                    content[lineIndex] = line[:start_index] + line[start_index + num_to_remove:]
            except ValueError:
                print("Invalid remove command.")
        return content

    def process_remove_word(self, content, command_line, lineIndex):
        match = re.search(r'removeWord\s+(.+)', command_line)
        if match and 0 <= lineIndex < len(content):
            line = content[lineIndex]
            word_to_remove = match.group(1)
            pattern = r'\b{}\b'.format(re.escape(word_to_remove))
            content[lineIndex] = re.sub(pattern, '', line).strip()
            content[lineIndex] = re.sub(r'\s+', ' ', content[lineIndex]).strip()
        return content

    def process_replace(self, content, command_line, lineIndex):
        match = re.search(r'replace\s+(\d+)\s+(.+)', command_line)
        if match and 0 <= lineIndex < len(content):
            index = int(match.group(1))
            replacement = match.group(2)
            line = content[lineIndex]

            if 0 <= index < len(line):
                part_before = line[:index]
                part_after = line[index + len(replacement):]
                content[lineIndex] = part_before + replacement + part_after
        return content

    def process_replace_word(self, content, command_line, lineIndex):
        match = re.search(r'replaceWord\s+(.+)\s+(.+)', command_line)
        if match and 0 <= lineIndex < len(content):
            word = match.group(1)
            replacement = match.group(2)
            line = content[lineIndex]
            pattern = r'\b{}\b'.format(re.escape(word))
            content[lineIndex] = re.sub(pattern, replacement, line)
        return content

    def process_reverse(self, content, command_line, lineIndex):
        match = re.search(r'reverse\s+(\d+)', command_line)
        if match and 0 <= lineIndex < len(content):
            try:
                word_index = int(match.group(1))
                line = content[lineIndex].split()
                if 0 <= word_index < len(line):
                    line[word_index] = line[word_index][::-1]
                    content[lineIndex] = ' '.join(line)
            except ValueError:
                print("Invalid reverse command.")
        return content

    def process_add_new_line(self, content, command_line, lineIndex):
        if "addNewLine" in command_line:
            content.insert(lineIndex + 1, '')  # Add a blank line after lineIndex
        return content

    def process_duplicate(self, content, command_line, lineIndex):
        match = re.search(r'duplicate\s+(.+)', command_line)
        if match and 0 <= lineIndex < len(content):
            word_to_duplicate = match.group(1)
            line = content[lineIndex]
            content[lineIndex] = line + " " + word_to_duplicate
        return content

    def process_swap_with_next_line(self, content, command_line, lineIndex):
        if "swapWithNextLine" in command_line and 0 <= lineIndex < len(content) - 1:
            content[lineIndex], content[lineIndex + 1] = content[lineIndex + 1], content[lineIndex]
        return content

    def process_swap_with_previous_line(self, content, command_line, lineIndex):
        if "swapWithPreviousLine" in command_line and 1 <= lineIndex < len(content):
            content[lineIndex], content[lineIndex - 1] = content[lineIndex - 1], content[lineIndex]
        return content

    def process_remove_white_spaces(self, content, command_line, lineIndex):
        if "removeWhiteSpaces" in command_line and 0 <= lineIndex < len(content):
            content[lineIndex] = re.sub(r'\s+', ' ', content[lineIndex]).strip()
        return content

    def process_write_to_console(self, content, command_line, lineIndex):
        if "writeToConsole" in command_line and 0 <= lineIndex < len(content):
            print(content[lineIndex])
        return content