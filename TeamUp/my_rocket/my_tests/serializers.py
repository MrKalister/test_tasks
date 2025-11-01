from rest_framework import serializers

from .models import EQTestResult, IQTestResult, UniqueLogin


class CreateTestSerializer(serializers.ModelSerializer):
    login = serializers.CharField(source='unique_string', read_only=True)

    class Meta:
        model = UniqueLogin
        fields = ('login', )


class ResultSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['login'] = CreateTestSerializer(
            instance.login).data['login']
        return ret


class EQTestResultSerializer(ResultSerializer):

    class Meta:
        model = EQTestResult
        fields = ('letters', 'timestamp', 'login')

    def validate_letters(self, value):

        valid_letters = ['а', 'б', 'в', 'г', 'д']

        errors = []
        if len(value) != 5:
            errors.append('The "letters" list must contain exactly 5 letters. '
                          f'You have {len(value)}')
        elif len(set(value)) != 5:
            errors.append('The "letters" in the list should not be repeated.')
        for letter in value:
            if letter not in valid_letters:
                errors.append(f'Invalid letter: {letter}. '
                              f'Valid letters are {valid_letters}')
        if errors:
            raise serializers.ValidationError(errors)
        return value


class IQTestResultSerializer(ResultSerializer):

    class Meta:
        model = IQTestResult
        fields = ('points', 'timestamp', 'login')


class GetTestSerializer(serializers.ModelSerializer):

    iq_test, eq_test = IQTestResultSerializer(), EQTestResultSerializer()
    login = serializers.CharField(source='unique_string', read_only=True)

    class Meta:
        model = UniqueLogin
        fields = ('login', 'iq_test', 'eq_test')

    def to_representation(self, instance):
        """Delete login in once test."""

        ret = super().to_representation(instance)
        iq_test, eq_test = ret.get('iq_test'), ret.get('eq_test')
        if iq_test:
            iq_test.pop('login', None)
        if eq_test:
            eq_test.pop('login', None)
        return ret
