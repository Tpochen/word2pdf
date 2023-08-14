import subprocess

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
import os


class Converter(View):
    async def get(self, request):
        return render(request, 'convert.html')

    async def post(self, request):
        # 判断请求体是否携带文件参数
        try:
            if request.FILES.get('word_file'):
                word_file = request.FILES.get('word_file')

                # 校验文件类型
                if not word_file.name.endswith('.docx'):
                    return JsonResponse({
                        'code': 400,
                        'msg': '错误的文件格式',
                        'data': None,
                    })

                # 将文件存储到本地
                file_path = os.path.join('uploads', word_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in word_file.chunks():
                        destination.write(chunk)

                # 使用unoconv进行转化
                pdf_file_path = file_path.replace('.docx', '.pdf')
                subprocess.run(['unoconv', '-f', 'pdf', file_path])

                # 删除原文件
                os.remove(file_path)

                # 返回转换后的pdf
                with open(pdf_file_path, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                    response = HttpResponse(pdf_data, content_type='application/pdf')
                    response['Content-Disposition'] = f'inline; filename="{word_file.name.replace(".docx", ".pdf")}"'

                # 删除生成的 PDF 文件
                os.remove(pdf_file_path)

                return response
            else:
                return JsonResponse({
                    'code': 400,
                    'msg': '未上传文件',
                    'data': None,
                })
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': str(e),
                'data': None,
            })
